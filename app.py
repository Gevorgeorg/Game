from flask import Flask, request, render_template, redirect, url_for

from classes.arena import Arena
from classes.classes import Warrior, Tank
from classes.equipment import Equipment
from classes.units import Player, Enemy

app = Flask(__name__)
equipment_data: Equipment = Equipment("data/equipment.json")
classes: dict = {
    'warrior': Warrior,
    'tank': Tank
}
arena: Arena = Arena()
heroes: dict = {}


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/choose-hero/', methods=['GET', 'POST'])
def choose_hero():
    if request.method == 'GET':
        result: dict = {
            "header": "Выбор героя",
            "classes": list(classes.keys()),
            "weapons": equipment_data.get_weapon_names(),
            "armors": equipment_data.get_armor_names()
        }
        return render_template("hero_choosing.html", result=result)

    elif request.method == 'POST':

        name: str = request.form.get('name')
        unit_class_name: str = request.form.get('unit_class')
        weapon_name: str = request.form.get('weapon')
        armor_name: str = request.form.get('armor')

        if not name:
            return "Необходимо указать имя"

        hero: Player = Player(
            name=name,
            unit_class=classes[unit_class_name],
            weapon=equipment_data.get_weapon(weapon_name),
            armor=equipment_data.get_armor(armor_name)
        )
        heroes["player"] = hero

        return redirect(url_for('choose_enemy'))


@app.route('/choose-enemy/', methods=['GET', 'POST'])
def choose_enemy():
    if request.method == 'GET':

        result: dict = {
            "header": "Выбор противника",
            "classes": list(classes.keys()),
            "weapons": equipment_data.get_weapon_names(),
            "armors": equipment_data.get_armor_names()
        }
        return render_template("hero_choosing.html", result=result)

    elif request.method == 'POST':

        name: str = request.form.get('name')
        unit_class_name: str = request.form.get('unit_class')
        weapon_name: str = request.form.get('weapon')
        armor_name: str = request.form.get('armor')

        if not name:
            return "Необходимо указать имя"

        hero: Enemy = Enemy(
            name=name,
            unit_class=classes[unit_class_name],
            weapon=equipment_data.get_weapon(weapon_name),
            armor=equipment_data.get_armor(armor_name)
        )
        heroes["enemy"] = hero

        return redirect(url_for('fight'))


@app.route('/fight/', methods=['GET'])
def fight():
    arena.start_game(heroes)
    return render_template("fight.html",
                           heroes=heroes,
                           result="Бой начался!",
                           battle_result="")


@app.route('/fight/hit/', methods=['GET'])
def fight_hit():
    result: str = arena.hitting()

    battle_result: str = arena.check_health()

    return render_template("fight.html",
                           heroes=heroes,
                           result=result,
                           battle_result=battle_result)


@app.route('/fight/use-skill/', methods=['GET'])
def fight_use_skill():
    result: str = arena.use_skill()

    battle_result: str = arena.check_health()

    return render_template("fight.html",
                           heroes=heroes,
                           result=result,
                           battle_result=battle_result)


@app.route('/fight/pass-turn/', methods=['GET'])
def fight_pass_turn():
    result: str = arena.skip_turn()

    battle_result: str = arena.check_health()

    return render_template("fight.html",
                           heroes=heroes,
                           result=result,
                           battle_result=battle_result)


@app.route('/fight/end-fight/', methods=['GET'])
def fight_end():
    arena.end_game()
    heroes.clear()
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
