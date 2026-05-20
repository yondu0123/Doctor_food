import argparse
import json
import os
import shutil
import sys
import time

try:
    import win32com.client as win32
except ImportError:
    print("[ERROR] pywin32가 필요합니다: pip install pywin32")
    sys.exit(1)


def load_sections(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def backup_file(path):
    base, ext = os.path.splitext(path)
    backup = f"{base}.backup{ext}"
    shutil.copy2(path, backup)
    return backup


def find_and_move(hwp, keyword):
    hwp.Run("MoveDocBegin")
    hwp.HAction.GetDefault("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)
    hwp.HParameterSet.HFindReplace.FindString = keyword
    hwp.HParameterSet.HFindReplace.Direction = hwp.FindDir("Forward")
    hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
    return hwp.HAction.Execute("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)


def insert_text_below_heading(hwp, text):
    hwp.Run("MoveLineEnd")
    hwp.Run("BreakPara")
    hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
    hwp.HParameterSet.HInsertText.Text = text
    hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)
    hwp.Run("BreakPara")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hwp", required=True, help="대상 HWP 파일 경로")
    parser.add_argument("--sections", required=True, help="sections.json 경로")
    parser.add_argument("--save-as", default="", help="결과 저장 경로(옵션)")
    args = parser.parse_args()

    hwp_path = os.path.abspath(args.hwp)
    sections = load_sections(args.sections)

    if not os.path.exists(hwp_path):
        print(f"[ERROR] 파일 없음: {hwp_path}")
        sys.exit(1)

    backup = backup_file(hwp_path)
    print(f"[INFO] backup 생성: {backup}")

    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.XHwpWindows.Item(0).Visible = True
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")

    hwp.Open(hwp_path)
    time.sleep(0.8)

    not_found = []
    for heading, body in sections.items():
        ok = find_and_move(hwp, heading)
        if not ok:
            not_found.append(heading)
            continue
        insert_text_below_heading(hwp, body)
        print(f"[OK] 삽입 완료: {heading}")
        time.sleep(0.2)

    out_path = os.path.abspath(args.save_as) if args.save_as else hwp_path
    hwp.SaveAs(out_path)
    print(f"[DONE] 저장 완료: {out_path}")

    if not_found:
        print("[WARN] 아래 섹션을 찾지 못했습니다:")
        for n in not_found:
            print(" -", n)


if __name__ == "__main__":
    main()
