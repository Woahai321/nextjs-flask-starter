from flask import Flask, request, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route("/api/process-csv", methods=["POST"])
def process_csv():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        # Read the CSV file
        df = pd.read_csv(file)

        # Perform some processing (example: convert all text to uppercase)
        df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

        # Convert the DataFrame back to CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        # Return the processed CSV file
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            as_attachment=True,
            download_name='processed_file.csv',
            mimetype='text/csv'
        )

if __name__ == "__main__":
    app.run(port=5328)
