from flask import Flask, render_template, url_for, request, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')


def showRestaurants():
	allrestaurants = session.query(Restaurant).all()

	return render_template('restaurants.html', allrestaurants = allrestaurants)

@app.route('/restaurants/new', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		new = Restaurant(name = request.form['name'])
		session.add(new)
		session.commit()
		flash("new Restaurant added!")
		return redirect(url_for("showRestaurants"))
	else:
		return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
	editedrestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedrestaurant.name = request.form['name']
			session.add(editedrestaurant)
			session.commit()
			flash("Restaurant name edited!")
			return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html',restaurant_id = restaurant_id, i = editedrestaurant)
	


@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
	deleterestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(deleterestaurant)
		session.commit()
		flash("Restaurant deleted!")
		return redirect(url_for('showRestaurants'))
	else:
	    return render_template('deleterestaurant.html', restaurant_id = restaurant_id, item = deleterestaurant)



@app.route('/restaurants/<int:restaurant_id>/menu')
def RestaurantMenu(restaurant_id):
     
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit' , methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editeditem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editeditem.name = request.form['name']
            editeditem.description = request.form['description']
            editeditem.price = request.form['price']
            editeditem.course = request.form['course']
            session.add(editeditem)
            session.commit()
            flash("menu item edited!")
            return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editeditem)


"""@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete' , methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):

	item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':

        if request.form['delete']:

        	session.delete(item)
            session.commit()
            flash("menu item deleted!")
            return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = item)"""



@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete' , methods = ['GET', 'POST'])

def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['delete']:
            session.delete(item)
            session.commit()
            flash("menu item deleted!")
            return redirect(url_for('RestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = item)











if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


