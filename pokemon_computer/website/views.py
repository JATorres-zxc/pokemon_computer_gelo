from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Pokemon
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        poke_id = request.form.get('poke_id')
        name = request.form.get('name')
        region = request.form.get('region')
        type1 = request.form.get('type1')
        type2 = request.form.get('type2')
        
        existing_pokemon = Pokemon.query.filter_by(poke_id=poke_id).first()

        if existing_pokemon:
            pokemon = existing_pokemon
            if pokemon.user_id == current_user.id:
                pokemon.Name = name
                pokemon.region = region
                pokemon.type1 = type1
                pokemon.type2 = type2
                db.session.commit()
                flash('Pokemon updated!', category='success')
        else:
            if len(name) < 1:
                flash('Pokemon name is too short!', category='error')
            else:
                new_pokemon = Pokemon(poke_id=poke_id,Name=name, region=region, type1=type1, type2=type2, user_id=current_user.id)
                db.session.add(new_pokemon)
                db.session.commit()
                flash('Pokemon added!', category='success')

        return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)

@views.route('/delete-pokemon', methods=['POST'])
def delete_pokemon():
    pokemon = json.loads(request.data)
    pokemon_id = pokemon['pokemonId']
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        if pokemon.user_id == current_user.id:
            db.session.delete(pokemon)
            db.session.commit()
    return jsonify({})

