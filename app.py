import base64
from io import BytesIO
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- HTML Template (The Frontend) ---
# I am embedding HTML here so you only need one file.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image <-> Text Converter</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; background: #f4f4f9; }
        h1 { text-align: center; color: #333; }
        .container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .section { margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid #eee; }
        textarea { width: 100%; height: 150px; margin-top: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: monospace; font-size: 12px; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; font-size: 1rem; }
        button:hover { background: #0056b3; }
        input[type="file"] { margin-bottom: 10px; }
        img { max-width: 100%; height: auto; margin-top: 10px; border: 5px solid #333; border-radius: 4px; }
        .copy-btn { background: #28a745; margin-top: 5px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <h1>Image Encryption Tool</h1>
    <div class="container">
    
        <div class="section">
            <h2>1. Image to Text (Encode)</h2>
            <form action="/encode" method="post" enctype="multipart/form-data">
                <p>Select an image to convert into a text string:</p>
                <input type="file" name="image_file" required>
                <button type="submit">Convert to Text</button>
            </form>
            {% if encoded_text %}
                <h3>Resulting Text Code:</h3>
                <textarea id="codeBox">{{ encoded_text }}</textarea>
                <button class="copy-btn" onclick="copyText()">Copy Code</button>
            {% endif %}
        </div>

        <div class="section">
            <h2>2. Text to Image (Decode)</h2>
            <form action="/decode" method="post">
                <p>Paste the text string here to get the image back:</p>
                <textarea name="text_code" placeholder="Paste the long code here..." required></textarea>
                <br><br>
                <button type="submit">Convert Back to Image</button>
            </form>
            {% if decoded_image_data %}
                <h3>Resulting Image:</h3>
                <img src="data:image/jpeg;base64,{{ decoded_image_data }}" alt="Restored Image">
            {% endif %}
        </div>

    </div>

    <script>
        function copyText() {
            var copyText = document.getElementById("codeBox");
            copyText.select();
            document.execCommand("copy");
            alert("Copied to clipboard!");
        }
    </script>
</body>
</html>
"""

# --- Routes (The Backend Logic) ---

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/encode', methods=['POST'])
def encode_image():
    file = request.files['image_file']
    if file:
        # Read file bytes
        data = file.read()
        # Convert bytes to base64 string
        # We decode('utf-8') to turn the bytes into a normal python string
        encoded_string = base64.b64encode(data).decode('utf-8')
        return render_template_string(HTML_TEMPLATE, encoded_text=encoded_string)
    return render_template_string(HTML_TEMPLATE)

@app.route('/decode', methods=['POST'])
def decode_image():
    text_code = request.form['text_code']
    if text_code:
        # We just pass the text back to the HTML
        # The <img> tag in HTML can read base64 directly, so we don't even need
        # to save it to a file on the server!
        return render_template_string(HTML_TEMPLATE, decoded_image_data=text_code)
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)