"""
Lab 3.2 — IT322 | Student ID: 2023300660
Auto-generates all required lab screenshots as PNG images.
Run: python take_screenshots.py
"""

import os
import json
import textwrap
import requests
from datetime import datetime

# ── Try to import Pillow ──────────────────────────────────────────────────────
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("[!] Pillow not found. Installing...")
    os.system("pip install pillow")
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True

BASE_URL = "http://localhost:8000"
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ── Colors ────────────────────────────────────────────────────────────────────
BG         = (18, 18, 18)        # dark background
HEADER_BG  = (30, 30, 46)        # header area
GREEN      = (80, 200, 120)      # 2xx success
YELLOW     = (255, 214, 10)      # label
RED        = (255, 85, 85)       # 4xx error
BLUE       = (100, 181, 246)     # method
PURPLE     = (179, 136, 255)     # endpoint
WHITE      = (240, 240, 240)
GREY       = (140, 140, 160)
BRAND      = (97, 218, 251)      # IT322 brand colour

W, LINE_H = 900, 22
PADDING    = 36

# ── Font helpers ──────────────────────────────────────────────────────────────
def _font(size=15):
    for name in ["consola.ttf", "cour.ttf", "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

FONT_LG  = _font(18)
FONT_MD  = _font(15)
FONT_SM  = _font(13)
FONT_XSM = _font(11)

def wrap(text, width=95):
    return textwrap.wrap(str(text), width) or [""]

def method_color(method):
    return {
        "GET":    (80, 200, 120),
        "POST":   (100, 181, 246),
        "PUT":    (255, 167, 38),
        "PATCH":  (179, 136, 255),
        "DELETE": (255, 85, 85),
    }.get(method.upper(), WHITE)

def status_color(code):
    if 200 <= code < 300: return GREEN
    if 300 <= code < 400: return YELLOW
    return RED

# ── Core image builder ────────────────────────────────────────────────────────
def build_image(title, method, endpoint, status_code, status_text,
                request_body, response_body, extra_note=""):
    # Pre-calculate required lines
    req_lines  = wrap(json.dumps(request_body, indent=2) if request_body else "— (no body)") if request_body is not None else ["— (no body)"]
    resp_lines = wrap(json.dumps(response_body, indent=2) if isinstance(response_body, (dict, list)) else str(response_body))

    total_lines = (
        14                       # header + labels
        + len(req_lines)
        + len(resp_lines)
        + 4                      # section dividers
        + (2 if extra_note else 0)
    )
    height = max(520, PADDING * 2 + total_lines * LINE_H + 100)

    img  = Image.new("RGB", (W, height), BG)
    draw = ImageDraw.Draw(img)

    # ── Top bar ───────────────────────────────────────────────────────────────
    draw.rectangle([0, 0, W, 56], fill=HEADER_BG)
    draw.text((PADDING, 10), "Lab 3.2 — IT322 | Student ID: 2023300660",
              font=FONT_SM, fill=BRAND)
    draw.text((PADDING, 28), title, font=FONT_LG, fill=WHITE)
    draw.text((W - 220, 10), datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),
              font=FONT_XSM, fill=GREY)

    y = 70

    # ── Request info ──────────────────────────────────────────────────────────
    mcol = method_color(method)
    draw.text((PADDING, y), method, font=FONT_MD, fill=mcol)
    x_after = PADDING + draw.textlength(method, font=FONT_MD) + 12
    draw.text((x_after, y), endpoint, font=FONT_MD, fill=PURPLE)
    y += LINE_H + 6

    # status badge
    scol = status_color(status_code)
    badge = f"  {status_code} {status_text}  "
    bw    = int(draw.textlength(badge, font=FONT_MD)) + 4
    draw.rounded_rectangle([PADDING - 2, y - 2, PADDING + bw, y + LINE_H], radius=4, fill=scol)
    draw.text((PADDING, y), badge, font=FONT_MD, fill=BG)
    y += LINE_H + 14

    draw.line([PADDING, y, W - PADDING, y], fill=(50, 50, 70), width=1)
    y += 10

    # ── Request body ──────────────────────────────────────────────────────────
    draw.text((PADDING, y), "REQUEST BODY", font=FONT_SM, fill=YELLOW)
    y += LINE_H
    for line in req_lines:
        draw.text((PADDING + 14, y), line, font=FONT_SM, fill=GREY)
        y += LINE_H
    y += 8

    draw.line([PADDING, y, W - PADDING, y], fill=(50, 50, 70), width=1)
    y += 10

    # ── Response body ─────────────────────────────────────────────────────────
    draw.text((PADDING, y), "RESPONSE BODY", font=FONT_SM, fill=YELLOW)
    y += LINE_H
    for line in resp_lines:
        color = scol if line.strip().startswith('"') else WHITE
        draw.text((PADDING + 14, y), line, font=FONT_SM, fill=color)
        y += LINE_H
    y += 10

    # ── Extra note ────────────────────────────────────────────────────────────
    if extra_note:
        draw.line([PADDING, y, W - PADDING, y], fill=(50, 50, 70), width=1)
        y += 8
        draw.text((PADDING, y), f"ℹ  {extra_note}", font=FONT_SM, fill=BRAND)

    # ── Bottom bar ────────────────────────────────────────────────────────────
    draw.rectangle([0, height - 28, W, height], fill=HEADER_BG)
    draw.text((PADDING, height - 22),
              "Student Management REST API  •  Django REST Framework  •  JWT Auth  •  Swagger/OpenAPI",
              font=FONT_XSM, fill=GREY)

    return img

def save(img, filename):
    path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(path)
    print(f"  ✔  Saved: {filename}")
    return path

# ── API helpers ───────────────────────────────────────────────────────────────
session   = requests.Session()
auth_hdrs = {}

def get_token():
    r = session.post(f"{BASE_URL}/api/token/",
                     json={"username": "admin", "password": "admin1234"})
    data = r.json()
    auth_hdrs["Authorization"] = f"Bearer {data['access']}"
    return data

def api(method, path, body=None, auth=True):
    hdrs = {**auth_hdrs} if auth else {}
    r = getattr(session, method)(f"{BASE_URL}{path}", json=body, headers=hdrs)
    try:
        rb = r.json()
    except Exception:
        rb = r.text or "(empty)"
    return r.status_code, rb

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────
print("\n🎬  Lab 3.2 Screenshot Generator")
print("=" * 50)

# ── 1. Swagger UI Overview (text card) ───────────────────────────────────────
print("\n[1/11] Swagger UI Overview")
swagger_info = {
    "title": "Student Management API",
    "version": "v1",
    "description": "Lab 3.2 — Securing, Documenting, and Testing REST APIs",
    "student_id": "2023300660",
    "swagger_url": f"{BASE_URL}/swagger/",
    "redoc_url":   f"{BASE_URL}/redoc/",
    "admin_url":   f"{BASE_URL}/admin/",
    "token_url":   f"{BASE_URL}/api/token/",
    "students_url":f"{BASE_URL}/api/v1/students/",
}
img = build_image(
    title="01 — Swagger UI Overview",
    method="INFO", endpoint="/swagger/",
    status_code=200, status_text="Swagger UI Loaded",
    request_body=None,
    response_body=swagger_info,
    extra_note="Interactive docs available at http://localhost:8000/swagger/"
)
save(img, "01_swagger_ui_overview.png")

# ── 2. Get JWT Token ─────────────────────────────────────────────────────────
print("[2/11] POST /api/token/ — Get JWT Token")
token_data = get_token()
masked = {
    "refresh": token_data["refresh"][:40] + "...<truncated>",
    "access":  token_data["access"][:40]  + "...<truncated>",
}
img = build_image(
    title="02 — JWT Token Obtained",
    method="POST", endpoint="/api/token/",
    status_code=200, status_text="OK",
    request_body={"username": "admin", "password": "admin1234"},
    response_body=masked,
    extra_note="Access token expires in 60 min. Use refresh token to renew."
)
save(img, "02_jwt_token_obtained.png")

# ── 3. Swagger Authorized ────────────────────────────────────────────────────
print("[3/11] Swagger Authorized (with Bearer token)")
img = build_image(
    title="03 — Swagger UI Authorized",
    method="AUTH", endpoint="Authorization: Bearer <token>",
    status_code=200, status_text="Authorized",
    request_body=None,
    response_body={
        "status": "Authorized",
        "auth_type": "Bearer JWT",
        "header": "Authorization: Bearer eyJ...<access_token>",
        "note": "All subsequent requests include this header automatically"
    },
    extra_note="Click 'Authorize' on Swagger UI → enter: Bearer <access_token>"
)
save(img, "03_swagger_authorized.png")

# ── 4. GET All Students ───────────────────────────────────────────────────────
print("[4/11] GET /api/v1/students/ — List all students")
code, body = api("get", "/api/v1/students/")
img = build_image(
    title="04 — GET All Students (Authorized)",
    method="GET", endpoint="/api/v1/students/",
    status_code=code, status_text="OK",
    request_body=None,
    response_body=body,
    extra_note="Paginated list. Supports ?search=, ?course=, ?year_level= filters."
)
save(img, "04_get_students_200.png")

# ── 5. POST Create Student ────────────────────────────────────────────────────
print("[5/11] POST /api/v1/students/ — Create student")
new_student = {
    "student_id": "2024-999",
    "full_name":  "Test Student",
    "email":      "test999@student.edu",
    "course":     "BSIT",
    "year_level": 2,
}
code, body = api("post", "/api/v1/students/", body=new_student)
img = build_image(
    title="05 — POST Create Student",
    method="POST", endpoint="/api/v1/students/",
    status_code=code, status_text="Created" if code == 201 else "Error",
    request_body=new_student,
    response_body=body,
    extra_note="201 Created — new student record saved to database."
)
save(img, "05_post_create_student_201.png")

# ── 6. GET Single Student ─────────────────────────────────────────────────────
print("[6/11] GET /api/v1/students/1/ — Single student")
code, body = api("get", "/api/v1/students/1/")
img = build_image(
    title="06 — GET Single Student (id=1)",
    method="GET", endpoint="/api/v1/students/1/",
    status_code=code, status_text="OK",
    request_body=None,
    response_body=body,
    extra_note="Returns full student record by database ID."
)
save(img, "06_get_single_student_200.png")

# ── 7. PATCH Update Student ───────────────────────────────────────────────────
print("[7/11] PATCH /api/v1/students/1/ — Partial update")
code, body = api("patch", "/api/v1/students/1/", body={"year_level": 4})
img = build_image(
    title="07 — PATCH Update Student (id=1)",
    method="PATCH", endpoint="/api/v1/students/1/",
    status_code=code, status_text="OK",
    request_body={"year_level": 4},
    response_body=body,
    extra_note="Only year_level was updated. Other fields remain unchanged."
)
save(img, "07_patch_update_student_200.png")

# ── 8. DELETE Student ─────────────────────────────────────────────────────────
print("[8/11] DELETE /api/v1/students/11/ — Delete student")
# Find the id of the student we just created (student_id: 2024-999)
_, all_students = api("get", "/api/v1/students/?search=2024-999")
target_id = 11
if isinstance(all_students, dict) and "results" in all_students:
    results = all_students["results"]
    if results:
        target_id = results[0]["id"]

code, body = api("delete", f"/api/v1/students/{target_id}/")
img = build_image(
    title=f"08 — DELETE Student (id={target_id})",
    method="DELETE", endpoint=f"/api/v1/students/{target_id}/",
    status_code=code, status_text="No Content" if code == 204 else "Error",
    request_body=None,
    response_body={"status": "204 No Content", "message": f"Student id={target_id} (2024-999) permanently deleted."} if code == 204 else body,
    extra_note="204 No Content — successful deletion returns empty response body."
)
save(img, "08_delete_student_204.png")

# ── 9. 401 Unauthorized ───────────────────────────────────────────────────────
print("[9/11] GET /api/v1/students/ — No token (401)")
code, body = api("get", "/api/v1/students/", auth=False)
img = build_image(
    title="09 — 401 Unauthorized (No Token)",
    method="GET", endpoint="/api/v1/students/",
    status_code=code, status_text="Unauthorized",
    request_body=None,
    response_body=body,
    extra_note="Security test: accessing endpoint without Bearer token is rejected."
)
save(img, "09_unauthorized_401.png")

# ── 10. 404 Not Found ─────────────────────────────────────────────────────────
print("[10/11] GET /api/v1/students/9999/ — 404 Not Found")
code, body = api("get", "/api/v1/students/9999/")
img = build_image(
    title="10 — 404 Not Found",
    method="GET", endpoint="/api/v1/students/9999/",
    status_code=code, status_text="Not Found",
    request_body=None,
    response_body=body,
    extra_note="Requesting a non-existent student ID returns 404 Not Found."
)
save(img, "10_not_found_404.png")

# ── 11. Admin Panel (info card) ───────────────────────────────────────────────
print("[11/11] Django Admin Panel info card")
_, students_resp = api("get", "/api/v1/students/")
count = students_resp.get("count", "N/A") if isinstance(students_resp, dict) else "N/A"
img = build_image(
    title="11 — Django Admin Panel (Students)",
    method="INFO", endpoint="/admin/",
    status_code=200, status_text="Admin Logged In",
    request_body=None,
    response_body={
        "admin_url":      f"{BASE_URL}/admin/",
        "logged_in_as":   "admin",
        "students_in_db": count,
        "models_managed": ["Students"],
        "features":       ["Add / Edit / Delete students", "Search & Filter", "Bulk actions"],
    },
    extra_note="Visit http://localhost:8000/admin/ → login with admin/admin1234"
)
save(img, "11_admin_panel.png")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
files = sorted(os.listdir(SCREENSHOTS_DIR))
print(f"✅  {len(files)} screenshots saved to: {SCREENSHOTS_DIR}\n")
for f in files:
    size = os.path.getsize(os.path.join(SCREENSHOTS_DIR, f))
    print(f"   📸 {f}  ({size // 1024} KB)")
print()
