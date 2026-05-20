on run argv
	if (count of argv) < 2 then
		error "usage: osascript hwp_section_writer_macos.applescript <hwp_path> <sections_json_path>"
	end if
	set hwpPath to item 1 of argv
	set jsonPath to item 2 of argv

	set sectionItems to paragraphs of (do shell script "python3 - <<'PY' " & quoted form of jsonPath & "\nimport json,sys\np=sys.argv[1]\nd=json.load(open(p,'r',encoding='utf-8'))\nfor k,v in d.items():\n    print(k.replace('\\n',' '))\n    print(v.replace('\\n','\\\\n'))\nPY")

	tell application "Hancom Office Hanword" to activate
	do shell script "open " & quoted form of hwpPath
	delay 2

	tell application "System Events"
		tell process "Hancom Office Hanword"
			set i to 1
			repeat while i ≤ (count of sectionItems)
				set headingText to item i of sectionItems
				set bodyText to item (i + 1) of sectionItems

				keystroke "f" using command down
				delay 0.3
				keystroke headingText
				key code 36
				delay 0.6
				key code 124
				key code 36
				delay 0.2

				keystroke bodyText
				key code 36
				delay 0.2

				set i to i + 2
			end repeat

			keystroke "s" using command down
		end tell
	end tell
end run
