# auth.py
from __future__ import annotations

import os
import re
import json
import time
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any

import streamlit as st

DEFAULT_DATA_DIR = "data"
IDENTITY_STATE_KEY = "student_identity"
APP_SALT_ENV = "COURSE_APP_SALT"

REQUIRE_EMAIL_DEFAULT = False


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def _safe_slug(text: str, max_len: int = 64) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:max_len] if text else "student"


def _get_salt() -> str:
    return os.getenv(APP_SALT_ENV, "streamlit-course-salt")


def _hash_id(name: str, email: str = "") -> str:
    raw = (name.strip().lower() + "|" + email.strip().lower() + "|" + _get_salt()).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12]


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _data_root() -> Path:
    root = Path(DEFAULT_DATA_DIR)
    _ensure_dir(root)
    return root


def _identity() -> Dict[str, Any]:
    if IDENTITY_STATE_KEY not in st.session_state:
        st.session_state[IDENTITY_STATE_KEY] = {
            "confirmed": False,
            "name": "",
            "email": "",
            "student_id": "",
            "student_hash": "",
            "created_at": "",
            "last_seen": "",
        }
    return st.session_state[IDENTITY_STATE_KEY]


def init_auth() -> None:
    _identity()
    ident = _identity()
    ident["last_seen"] = _now_iso()
    st.session_state[IDENTITY_STATE_KEY] = ident


def is_authenticated() -> bool:
    ident = _identity()
    return bool(ident.get("confirmed") and ident.get("name") and ident.get("student_hash"))


def get_student_identity() -> Dict[str, Any]:
    return _identity()


def student_storage_dir() -> Path:
    ident = _identity()
    base = _data_root() / "students"
    _ensure_dir(base)

    if not ident.get("student_hash"):
        temp = base / "unconfirmed"
        _ensure_dir(temp)
        return temp

    folder = f"{_safe_slug(ident.get('name','student'))}_{ident['student_hash']}"
    path = base / folder
    _ensure_dir(path)
    return path


def course_event_log_path() -> Path:
    root = _data_root() / "logs"
    _ensure_dir(root)
    return root / "events.jsonl"


def log_event(event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
    payload = payload or {}
    ident = _identity()

    record = {
        "ts": _now_iso(),
        "event": event_type,
        "student_name": ident.get("name", ""),
        "student_email": ident.get("email", ""),
        "student_id": ident.get("student_id", ""),
        "student_hash": ident.get("student_hash", ""),
        "payload": payload,
    }

    # Global log
    global_path = course_event_log_path()
    with global_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Student log
    sdir = student_storage_dir()
    spath = sdir / "events.jsonl"
    with spath.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def reset_identity() -> None:
    st.session_state[IDENTITY_STATE_KEY] = {
        "confirmed": False,
        "name": "",
        "email": "",
        "student_id": "",
        "student_hash": "",
        "created_at": "",
        "last_seen": "",
    }
    log_event("identity_reset", {})


def render_identity_sidebar(
    *,
    title: str = "Student Access",
    require_email: bool = REQUIRE_EMAIL_DEFAULT,
    require_student_id: bool = False,
    show_reset: bool = True,
) -> None:
    init_auth()
    ident = _identity()

    with st.sidebar:
        st.markdown(f"### {title}")

        if is_authenticated():
            st.success("Identity confirmed")
            st.write(f"**Name:** {ident.get('name','')}")
            if ident.get("email"):
                st.write(f"**Email:** {ident.get('email','')}")
            if ident.get("student_id"):
                st.write(f"**ID:** {ident.get('student_id','')}")
            if show_reset:
                if st.button("Reset identity", use_container_width=True):
                    reset_identity()
                    st.rerun()
            return

        st.info("Enter your info and click **Confirm / Start**. This unlocks downloads and submissions.")

        name = st.text_input("Full name", value=ident.get("name", ""), placeholder="e.g., Jane Smith")

        if require_email:
            email = st.text_input("Email", value=ident.get("email", ""), placeholder="e.g., jsmith@school.edu")
        else:
            email = st.text_input("Email (optional)", value=ident.get("email", ""), placeholder="optional")

        if require_student_id:
            sid = st.text_input("Student ID", value=ident.get("student_id", ""), placeholder="required")
        else:
            sid = st.text_input("Student ID (optional)", value=ident.get("student_id", ""), placeholder="optional")

        if st.button("Confirm / Start", type="primary", use_container_width=True):
            if not name.strip():
                st.error("Please enter your full name.")
                return
            if require_email and (not email.strip() or "@" not in email):
                st.error("Please enter a valid email address.")
                return
            if require_student_id and not sid.strip():
                st.error("Please enter your student ID.")
                return

            ident["name"] = name.strip()
            ident["email"] = email.strip()
            ident["student_id"] = sid.strip()
            ident["student_hash"] = _hash_id(ident["name"], ident["email"])
            ident["confirmed"] = True
            ident["created_at"] = ident["created_at"] or _now_iso()
            ident["last_seen"] = _now_iso()
            st.session_state[IDENTITY_STATE_KEY] = ident

            _ = student_storage_dir()
            log_event("identity_confirmed", {"require_email": require_email, "require_student_id": require_student_id})

            st.success("Confirmed!")
            st.rerun()


def require_identity(
    *,
    require_email: bool = REQUIRE_EMAIL_DEFAULT,
    require_student_id: bool = False,
    block_message: str = "Please confirm your identity in the sidebar to access this page.",
) -> bool:
    render_identity_sidebar(require_email=require_email, require_student_id=require_student_id)
    if not is_authenticated():
        st.warning(block_message)
        st.stop()
    return True


def save_uploaded_file(
    uploaded_file,
    *,
    assignment_key: str,
    subfolder: str = "submissions",
    keep_original_name: bool = True,
) -> Path:
    if not is_authenticated():
        raise RuntimeError("Identity not confirmed. Call require_identity() first.")

    sdir = student_storage_dir() / subfolder / assignment_key
    _ensure_dir(sdir)

    filename = uploaded_file.name if keep_original_name else "upload.bin"
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", filename).strip("_")
    outpath = sdir / safe_name

    with outpath.open("wb") as f:
        f.write(uploaded_file.getbuffer())

    log_event("file_submitted", {"assignment_key": assignment_key, "filename": safe_name})
    return outpath


def save_text_submission(
    text: str,
    *,
    assignment_key: str,
    filename: str = "response.txt",
    subfolder: str = "submissions",
) -> Path:
    if not is_authenticated():
        raise RuntimeError("Identity not confirmed. Call require_identity() first.")

    sdir = student_storage_dir() / subfolder / assignment_key
    _ensure_dir(sdir)

    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", filename).strip("_")
    outpath = sdir / safe_name

    with outpath.open("w", encoding="utf-8") as f:
        f.write(text)

    log_event("text_submitted", {"assignment_key": assignment_key, "filename": safe_name})
    return outpath
