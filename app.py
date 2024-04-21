from flask import Flask,redirect,url_for,render_template,request
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb+srv://test:sparta@cluster0.atiyrt3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.adminPanel
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    fruit = list(db.fruit.find({}))
    return render_template('dashboard.html', fruit=fruit)

@app.route('/fruit',methods=['GET','POST'])
def fruit():
    fruit = list(db.fruit.find({}))
    return render_template('fruit.html', fruit=fruit)

@app.route('/addFruit',methods=['GET','POST'])
def addFruit():
    if request.method == 'POST':
        nama = request.form['nama'] #Mengambil data dari client
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']

        nama_gambar = request.files['gambar']

        if nama_gambar:
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
        else:
            nama_gambar = None

        doc = {
            'nama':nama,
            'harga':harga,
            'gambar':nama_file_gambar,
            'deskripsi':deskripsi
        }
        db.fruit.insert_one(doc)
        return redirect(url_for('fruit'))

    return render_template('AddFruit.html')

@app.route('/editFruit/<_id>',methods=['GET','POST'])
def editFruit(_id):
    if request.method == 'POST':
        id = request.form['_id'] 
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']

        nama_gambar = request.files['gambar']

        doc = {
            'nama':nama,
            'harga':harga,
            'deskripsi':deskripsi,
            

        }
        if nama_gambar:
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
            doc['gambar'] = nama_file_gambar
        db.fruit.update_one({"_id":ObjectId(id)},{'$set':doc})
        return redirect(url_for('fruit'))

    id = ObjectId(_id)
    data = list(db.fruit.find({'_id':id}))
    return render_template('EditFruit.html', data=data)

@app.route('/deleteFruit/<_id>',methods=['GET','POST'])
def deleteFruit(_id):
    db.fruit.delete_one({'_id':ObjectId(_id)})
    return redirect(url_for('fruit')) 

if __name__ == '__main__':
    # DEBUG is SET to TRUE, CHANGE FOR PROD
    app.run(port=5000, debug=True)
