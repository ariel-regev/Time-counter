import json, os, time

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

now = time.time() * 1000
last, record = d.get('last') or 0, d.get('record') or 0
cur = now - last

# שולח רק פעם אחת לכל רצף: ברגע שעוברים את השיא הקודם
send = last > 0 and record > 0 and cur > record and d.get('notifiedFor') != last

def fmt(ms):
    t = int(ms // 1000)
    return f"{t // 86400} ימים, {t % 86400 // 3600} שעות, {t % 3600 // 60} דקות"

with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as out:
    if send:
        d['notifiedFor'] = last
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        title = d.get('title') or 'המונה'
        body = f"שברת שיא! 🏆\n\n{title}\nהשיא הקודם היה: {fmt(record)}\nעכשיו אתה כבר על: {fmt(cur)}"
        out.write("send=true\n")
        out.write(f"body<<EOF\n{body}\nEOF\n")
    else:
        out.write("send=false\n")
