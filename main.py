from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
         dictionary ={ }
         for column in self.__table__.columns:
             dictionary[column.name] = getattr(self, column.name)
         return dictionary
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/random', methods=['GET'])
def random_cafe():
    all_cafes = Cafe.query.all()
    random_cafe = random.choice(all_cafes)
    return jsonify(random_cafe.to_dict())
    # return jsonify(cafe={"can_take_calls": random_cafe.can_take_calls,
    #                      "coffee_price":random_cafe.coffee_price,
    #                      "has_sockets":random_cafe.has_sockets,
    #                      "has_toilet":random_cafe.has_toilet,
    #                      "has_wifi":random_cafe.has_wifi,
    #                      "id":random_cafe.id,
    #                      "img_url":random_cafe.img_url,
    #                      "location":random_cafe.location,
    #                      "map_url":random_cafe.map_url,
    #                      "name":random_cafe.name,
    #                      "seats":random_cafe.seats
    #
    #                      })
@app.route('/all')
def all_cafes():
    dict ={}
    all_cafes = Cafe.query.all()
    for cafe in all_cafes:
        dict[cafe.id] = cafe.to_dict()


    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route('/search')
def search():
    loc = request.args['loc']
    print(loc)
    cafes  = Cafe.query.filter_by(location= loc).all()
    print(cafes)
    cafes = [cafe.to_dict() for cafe in cafes]
    if cafes == []:
        error = {
            "error":{
                      "not found" : "Sorry, we don't have a cafe at that location"
                    }
                }
        return jsonify(error)
    else:
        return jsonify(cafes)

@app.route('/add',methods =['GET','POST'])
def add_cafe():
    new_cafe = Cafe(name = request.form.get('name'),
                    map_url = request.form.get('map'),
                    img_url = request.form.get('img'),
                    location = request.form.get('loc'),
                    has_sockets = bool(request.form.get('sockets')),
                    has_toilet= bool(request.form.get('toilets')),
                    has_wifi = bool(request.form.get('wifi')),
                    can_take_calls = bool(request.form.get('calls')),
                    seats = request.form.get('seats'),
                    coffee_price = request.form.get('price'))

    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(Response ={"Success":"successfully Added the new cafe"})

@app.route('/update-price/<int:cafe_id>',methods= ["PATCH"])
def update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = request.args['new_price']
        return jsonify({"success":"Successfully Updated the price"})
    else:
        return jsonify(error={"Not Found":"Sorry a cafe with that id was not found in database."}),404

@app.route("/report-closed/<int:cafe_id>",methods =['DELETE'])
def delete_cafe(cafe_id):
    api_key = "TopSecretAPIKey"
    api_got= request.args['api-key']
    if api_key == api_got:
        cafe_to_delete = db.session.query(Cafe).get(cafe_id)
        print("test 1 complete")
        print(cafe_to_delete.id)
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            print("test 2 complete")
            return jsonify(success= {"success": 'Successfully deleted the cafe'})
        else:
            print("test 3 complete")
            return jsonify(error={"not found":"Sorry a cafe with that id was not found in the database."})
    else:
        print("test 4 complete")
        return jsonify(error="Sorry,That's not allowed. make sure you have the correct api_key")
## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
