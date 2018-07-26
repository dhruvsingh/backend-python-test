# -*- coding: utf-8 -*-
"""models for app."""

from alayatodo import db


class User(db.Model):
    """User model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        """__repr__ for User."""
        return '<User %r>' % self.username


class Todo(db.Model):
    """Todo model."""

    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column('user_id', db.ForeignKey(User.id))
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """__repr__ for Todo."""
        return '<User %r>' % self.user
