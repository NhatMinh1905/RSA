from flask import Flask, render_template, request, redirect, session, send_from_directory
import os, json, rsa
from rsa_utils import generate_keys, sign_file, verify_signature

app = Flask(__name__)
app.secret_key = "super_secret_key"
UPLOAD_FOLDER = 'files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists("users.json"):
    with open("users.json", "w") as f: json.dump({}, f)

@app.route('/')
def home():
    return redirect('/login') if 'user' not in session else redirect('/dashboard')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        with open("users.json") as f:
            users = json.load(f)
        if username in users:
            return "User exists"
        pub_key, priv_key = generate_keys()
        users[username] = {
            "password": password,
            "public_key": pub_key.decode(),
            "private_key": priv_key.decode()
        }
        with open("users.json", "w") as f: json.dump(users, f)
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        with open("users.json") as f:
            users = json.load(f)
        if username in users and users[username]["password"] == password:
            session['user'] = username
            return redirect('/dashboard')
        return "Wrong credentials"
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect('/login')
    with open("users.json") as f:
        users = json.load(f)
    return render_template("dashboard.html", users=users.keys())

@app.route('/send', methods=["GET", "POST"])
def send():
    if 'user' not in session: return redirect('/login')
    if request.method == "POST":
        receiver = request.form['receiver']
        file = request.files['file']
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        with open("users.json") as f: users = json.load(f)
        priv_key = users[session['user']]['private_key'].encode()
        signature = sign_file(filepath, priv_key)

        sig_path = filepath + ".sig"
        with open(sig_path, "wb") as f: f.write(signature)

        history = []
        if os.path.exists("history.json"):
            with open("history.json") as f: history = json.load(f)
        history.append({
            "sender": session['user'],
            "receiver": receiver,
            "file": filename
        })
        with open("history.json", "w") as f: json.dump(history, f)

        return "File sent!"
    return render_template("send_file.html")

@app.route('/receive')
def receive():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    files = []
    history_path = f"history/{user}.json"
    if os.path.exists(history_path):
        with open(history_path) as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    if record.get("receiver") == user:
                        stored_filename = f"{user}_{record['filename']}"
                        if os.path.exists(os.path.join("files", stored_filename)):
                            record["stored_filename"] = stored_filename
                            files.append(record)
                except:
                    continue
    return render_template("receive_file.html", files=files)


@app.route('/download/<filename>')
def download(filename):
    if 'user' not in session:
        return redirect('/login')
    file_path = os.path.join("files", filename)
    if os.path.exists(file_path):
        return send_from_directory("files", filename, as_attachment=True)
    return "File không tồn tại", 404


@app.route('/history')
def history():
    if not os.path.exists("history.json"): return "No history yet"
    with open("history.json") as f: data = json.load(f)
    return render_template("history.html", history=data)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/send', methods=['GET', 'POST'])
def send_file():
    if 'user' not in session:
        return redirect('/login')
    sender = session['user']
    if request.method == 'POST':
        receiver = request.form['receiver']
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join('files', f"{receiver}_{filename}")
        file.save(file_path)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record = {
            "sender": sender,
            "receiver": receiver,
            "filename": filename,
            "timestamp": timestamp
        }

        os.makedirs('history', exist_ok=True)
        for user in [sender, receiver]:
            hist_path = os.path.join("history", f"{user}.json")
            with open(hist_path, "a") as f:
                f.write(json.dumps(record) + "\n")

        return redirect('/dashboard')

    # Load danh sách người nhận từ users.json
    with open("users.json") as f:
        users = json.load(f)
    user_list = [u for u in users.keys() if u != sender]
    return render_template("send_file.html", users=user_list)