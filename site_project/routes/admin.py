from flask import (render_template, 
                   url_for, 
                   flash, 
                   redirect, 
                   request, 
                   Blueprint)

from flask_login import login_required, current_user
from models.models import db, Order, Feedback, User
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return User.access_denied()
    
    orders = Order.query.all()
    feedbacks = Feedback.query.all()
    return render_template('admin.html', orders=orders, feedbacks=feedbacks)


@admin_bp.route('/admin/order/<int:order_id>')
@login_required
def order_details(order_id):
    if not current_user.is_admin:
        return User.access_denied()
    
    order = Order.query.get(order_id)
    if not order:
        return Order.order_not_found('admin.admin')

    products = json.loads(order.products)
    return render_template('order_details.html', order=order, products=products)


@admin_bp.route('/admin/order/change-status/<int:order_id>', methods=['POST'])
@login_required
def order_change_status(order_id):
    if not current_user.is_admin:
        return User.access_denied()
    
    order = Order.query.get(order_id)
    if not order:
        return Order.order_not_found('admin.admin')
    
    order.update_status(request.form['status'])
    flash("Order status has been updated.", "success")
    return redirect(url_for('admin.order_details', order_id=order_id))


@admin_bp.route('/admin/order/delete/<int:order_id>')
@login_required
def order_delete(order_id):

    if not current_user.is_admin:
        return User.access_denied()
    
    order = Order.query.get(order_id)
    if not order:
        return Order.order_not_found('admin.admin')
    
    db.session.delete(order)
    db.session.commit()

    flash("Order has been deleted.", "success")
    return redirect(url_for('admin.admin'))


@admin_bp.route('/admin/feedback/delete/<int:feedback_id>')
@login_required
def feedback_delete(feedback_id):
    if not current_user.is_admin:
        return User.access_denied()
    
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        flash("Feedback not found.", "danger")
        return redirect(url_for('admin.admin'))
    
    db.session.delete(feedback)
    db.session.commit()

    flash("Feedback has been deleted.", "success")
    return redirect(url_for('admin.admin'))