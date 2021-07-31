from flask import Flask,render_template,request,flash
from werkzeug.utils import secure_filename
from keras.models import load_model
import cv2
import tensorflow
import os
app = Flask(__name__)
diseases=['blast', 'blight', 'Brownspot', 'sheath_blight', 'tungro']
 
from flask_ngrok import run_with_ngrok
run_with_ngrok(app)   
 
@app.route('/',methods=['POST','GET'])
def hello():
    return render_template('index.html')
 
@app.route('/predictLeaf',methods=['POST'])
def predictLeaf():
  if request.method=='POST' :
    model=load_model("./static/myModel.h5")
    print("hello")
    if 'file' not in request.files:
            print("no file")
    file = request.files['image']
    print(file)
    if file.filename == '':
            return render_template('index.html')
    filename = secure_filename(file.filename)
    print(filename)
    file.save(os.path.join('./static/userimageupload', filename))
    image=os.path.join('./static/userimageupload', filename)
    
    image=cv2.imread(image)
    image=cv2.resize(image,(256,256))
    
    image=image.reshape(1,256,256,3)
    image=image/255
    result=model.predict_classes(image)
    ans=diseases[result[0]]
    disease=ans
    uploaded_img="UPLOADED IMAGE:"
    insertimage=os.path.join('./static/userimageupload', filename)
    predicted_as="PREDICTED AS"
    predict_ans=ans
    
    if disease=='blast':
	    sol="Spray Tricyclazole75 0.6g/litre"+"\n"+"Isoprothiolane 40 EC 1.5ml/litre"

    elif disease=='sheath_blight':
      sol="Thifluzamide 24 SC 0.75 g/litre"+"\n"+"Validamycin 3 L 2.5 ml/litre"

    elif disease=="Brownspot":
      sol="Mancozeb 75 WP 2.5 g/litre"+"\n"+"Carbendazim 50 WP 2 g/kg"

    elif disease=="tungro":
      sol="Incorporate Phorate 10 G @ 12-15 kg/ha"+"\n"+"Fipronil 0.4 G @ 25 kg/ha"
    elif disease=="blight" :
      sol ="Incorporate 60-80 kg N/ha with required level of potassium"
  

 
  return render_template('index.html',uploaded_img="UPLOADED IMAGE:",one=1,insertimage=os.path.join('./static/userimageupload', filename),predicted_as="PREDICTED AS",predict_ans=ans,solution_text="ADVISORY MEASURES:",solution=sol)
       
        
 
app.run()