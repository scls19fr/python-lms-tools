from lms_tools.aiken import AikenQuiz, AikenQuestion
from lms_tools.gift import GiftQuiz, GiftQuestion, GiftDistractor


def test_gift_question_to_string():
    q = GiftQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :", name="0001", comment="question: 1 name: 0001")
    q.append_distractor(GiftDistractor("une girouette.", 0))
    q.append_distractor(GiftDistractor("une rose des vents.", 0))
    q.append_distractor(GiftDistractor("un baromètre.", 0))
    q.append_distractor(GiftDistractor("un anémomètre.", 1))
    assert q.is_binary()
    assert not q.is_correct_answer(0)
    assert not q.is_correct_answer(1)
    assert not q.is_correct_answer(2)
    assert q.is_correct_answer(3)
    expected_gift_text = """// question: 1 name: 0001
::0001::L'appareil servant à mesurer la vitesse du vent au sol s'appelle \:{
\t~une girouette.
\t~une rose des vents.
\t~un baromètre.
\t=un anémomètre.
}"""
    assert q.to_string() == expected_gift_text


def test_gift_question_set_correct_answer_binary():
    q = GiftQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :", name="0001", comment="question: 1 name: 0001")
    q.append_distractor("une girouette.")
    q.append_distractor("une rose des vents.")
    q.append_distractor("un baromètre.")
    q.append_distractor("un anémomètre.")
    q.set_correct_answer(3)
    assert not q.is_correct_answer(0)
    assert not q.is_correct_answer(1)
    assert not q.is_correct_answer(2)
    assert q.is_correct_answer(3)


def test_gift_question_to_string_with_escaped_char():
    q = GiftQuestion("Identifier les éléments 1, 2 et 3 de la structure :", name="0001", comment="question: 1 name: 0001")
    q.append_distractor("1 = nervure, 2 = couple, 3 = lisse.")
    q.append_distractor("1 = longeron, 2 = nervure, 3 = entretoise.")
    q.append_distractor("1 = poutre, 2 = traverse, 3 = semelle.")
    q.append_distractor("1 = couple, 2 = entretoise, 3 = traverse.")
    q.set_correct_answer(1)
    expected_gift_text = """// question: 1 name: 0001
::0001::Identifier les éléments 1, 2 et 3 de la structure \:{
\t~1 \= nervure, 2 \= couple, 3 \= lisse.
\t=1 \= longeron, 2 \= nervure, 3 \= entretoise.
\t~1 \= poutre, 2 \= traverse, 3 \= semelle.
\t~1 \= couple, 2 \= entretoise, 3 \= traverse.
}"""
    assert q.to_string() == expected_gift_text


def test_gift_question_not_is_binary():
    q = GiftQuestion("Question", name="0001", comment="question: 1 name: 0001")
    q.append_distractor(GiftDistractor("Bonne réponse", 1))
    q.append_distractor(GiftDistractor("Bonne réponse", 1))
    q.append_distractor(GiftDistractor("Bonne réponse", 1))
    q.append_distractor(GiftDistractor("Mauvaise réponse", 0))
    q.append_distractor(GiftDistractor("Mauvaise réponse", 0))
    assert not q.is_binary()
    assert not q.is_correct_answer(0)
    assert q.is_partially_correct_answer(0)
    assert q.is_partially_correct_answer(1)
    assert q.is_partially_correct_answer(2)
    assert not q.is_partially_correct_answer(3)
    assert not q.is_partially_correct_answer(4)

    expected_gift_text = """// question: 1 name: 0001
::0001::Question{
\t~33.33333%Bonne réponse
\t~33.33333%Bonne réponse
\t~33.33333%Bonne réponse
\t~0%Mauvaise réponse
\t~0%Mauvaise réponse
}"""
    assert q.to_string() == expected_gift_text


def test_gift_question_set_correct_answer_not_binary():
    q = GiftQuestion("Question", name="0001", comment="question: 1 name: 0001")
    q.append_distractor("Bonne réponse")
    q.append_distractor("Bonne réponse")
    q.append_distractor("Bonne réponse")
    q.append_distractor("Mauvaise réponse")
    q.append_distractor("Mauvaise réponse")
    q.set_correct_answer(0)
    q.set_correct_answer(1)
    q.set_correct_answer(2)
    assert q.is_partially_correct_answer(0)
    assert q.is_partially_correct_answer(1)
    assert q.is_partially_correct_answer(2)
    assert q.is_incorrect_answer(3)
    assert q.is_incorrect_answer(4)


def test_gift_quiz():
    quiz = GiftQuiz()
    q = GiftQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :", name="0001", comment="question: 1 name: 0001")
    q.append_distractor(GiftDistractor("une girouette.", 0))
    q.append_distractor(GiftDistractor("une rose des vents.", 0))
    q.append_distractor(GiftDistractor("un baromètre.", 0))
    q.append_distractor(GiftDistractor("un anémomètre.", 1))
    quiz.append(q)

    q = GiftQuestion("L'unité de pression utilisée dans le système international et en aéronautique est :", name="0002", comment="question: 2 name: 0002")
    q.append_distractor(GiftDistractor("le pascal.", 1))
    q.append_distractor(GiftDistractor("le newton.", 0))
    q.append_distractor(GiftDistractor("le joule.", 0))
    q.append_distractor(GiftDistractor("le millimètre de mercure.", 0))
    quiz.append(q)

    assert len(quiz) == 2

    header = """// question: 0  name: Switch category to $module$/Défaut pour BIA 2016 Météorologie et aérologie
$CATEGORY: $module$/Défaut pour BIA 2016 Météorologie et aérologie
"""

    footer = """
// end of quiz"""

    expected_gift_text = """// question: 0  name: Switch category to $module$/Défaut pour BIA 2016 Météorologie et aérologie
$CATEGORY: $module$/Défaut pour BIA 2016 Météorologie et aérologie

// question: 1 name: 0001
::0001::L'appareil servant à mesurer la vitesse du vent au sol s'appelle \:{
\t~une girouette.
\t~une rose des vents.
\t~un baromètre.
\t=un anémomètre.
}

// question: 2 name: 0002
::0002::L'unité de pression utilisée dans le système international et en aéronautique est \:{
\t=le pascal.
\t~le newton.
\t~le joule.
\t~le millimètre de mercure.
}

// end of quiz"""
    assert quiz.to_string(header=header, footer=footer) == expected_gift_text


def test_aiken_question_to_gift_question():
    q = AikenQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :")
    q.append_distractor("une girouette.")
    q.append_distractor("une rose des vents.")
    q.append_distractor("un baromètre.")
    q.append_distractor("un anémomètre.")
    q.set_correct_answer(3)
    gift_question = GiftQuestion.from_aiken(q)
    assert isinstance(gift_question, GiftQuestion)
    assert q.stem == gift_question.stem
    assert len(gift_question) == len(q)
    assert gift_question.is_binary()
    assert gift_question.is_correct_answer(3)


def test_aiken_quiz_to_gift_quiz():
    aiken_text = """L'appareil servant à mesurer la vitesse du vent au sol s'appelle :
A) une girouette.
B) une rose des vents.
C) un baromètre.
D) un anémomètre.
ANSWER: D

L'unité de pression utilisée dans le système international et en aéronautique est :
A) le pascal.
B) le newton.
C) le joule.
D) le millimètre de mercure.
ANSWER: A"""
    aiken_quiz = AikenQuiz.parse(aiken_text)
    gift_quiz = GiftQuiz.from_aiken(aiken_quiz)
    for i, question in enumerate(gift_quiz.iter_questions()):
        val = i + 1
        question.comment = "question: %d name: %04d" % (val, val)
        question.name = "%04d" % val
    gift_text = gift_quiz.to_string()
    expected_gift_text = """// question: 1 name: 0001
::0001::L'appareil servant à mesurer la vitesse du vent au sol s'appelle \:{
\t~une girouette.
\t~une rose des vents.
\t~un baromètre.
\t=un anémomètre.
}

// question: 2 name: 0002
::0002::L'unité de pression utilisée dans le système international et en aéronautique est \:{
\t=le pascal.
\t~le newton.
\t~le joule.
\t~le millimètre de mercure.
}"""
    assert expected_gift_text == gift_text
    assert len(aiken_quiz) == len(gift_quiz)


def test_gift_quiz_join():
    quiz1 = GiftQuiz()
    q = GiftQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :", name="0001", comment="question: 1 name: 0001")
    q.append_distractor(GiftDistractor("une girouette.", 0))
    q.append_distractor(GiftDistractor("une rose des vents.", 0))
    q.append_distractor(GiftDistractor("un baromètre.", 0))
    q.append_distractor(GiftDistractor("un anémomètre.", 1))
    quiz1.append(q)

    q = GiftQuestion("L'unité de pression utilisée dans le système international et en aéronautique est :", name="0002", comment="question: 2 name: 0002")
    q.append_distractor(GiftDistractor("le pascal.", 1))
    q.append_distractor(GiftDistractor("le newton.", 0))
    q.append_distractor(GiftDistractor("le joule.", 0))
    q.append_distractor(GiftDistractor("le millimètre de mercure.", 0))
    quiz1.append(q)

    quiz2 = GiftQuiz()
    q = GiftQuestion("En vol en palier stabilisé :", name="0003", comment="question: 3 name: 0003")
    q.append_distractor(GiftDistractor("la portance équilibre le poids.", 1))
    q.append_distractor(GiftDistractor("la portance équilibre la traînée.", 0))
    q.append_distractor(GiftDistractor("la portance équilibre la résultante aérodynamique.", 0))
    q.append_distractor(GiftDistractor("la portance équilibre la force de propulsion.", 0))
    quiz2.append(q)

    q = GiftQuestion("Le vent relatif :", name="0004", comment="question: 4 name: 0004")
    q.append_distractor(GiftDistractor("est la composante du vent réel parallèle à la trajectoire.", 0))
    q.append_distractor(GiftDistractor("est parallèle à la trajectoire, et de même sens que le déplacement de l'avion.", 0))
    q.append_distractor(GiftDistractor("est parallèle à la trajectoire, mais de sens opposé au déplacement de l'avion.", 1))
    q.append_distractor(GiftDistractor("est la composante du vent réel perpendiculaire à la trajectoire.", 0))
    quiz2.append(q)

    quiz_result = GiftQuiz.join([quiz1, quiz2])

    expected_text = """// question: 1 name: 0001
::0001::L'appareil servant à mesurer la vitesse du vent au sol s'appelle \:{
\t~une girouette.
\t~une rose des vents.
\t~un baromètre.
\t=un anémomètre.
}

// question: 2 name: 0002
::0002::L'unité de pression utilisée dans le système international et en aéronautique est \:{
\t=le pascal.
\t~le newton.
\t~le joule.
\t~le millimètre de mercure.
}

// question: 3 name: 0003
::0003::En vol en palier stabilisé \:{
\t=la portance équilibre le poids.
\t~la portance équilibre la traînée.
\t~la portance équilibre la résultante aérodynamique.
\t~la portance équilibre la force de propulsion.
}

// question: 4 name: 0004
::0004::Le vent relatif \:{
\t~est la composante du vent réel parallèle à la trajectoire.
\t~est parallèle à la trajectoire, et de même sens que le déplacement de l'avion.
\t=est parallèle à la trajectoire, mais de sens opposé au déplacement de l'avion.
\t~est la composante du vent réel perpendiculaire à la trajectoire.
}"""
    assert len(quiz_result) == 4
    assert quiz_result.to_string() == expected_text


def test_gift_parse():
    gift_text = """// question: 1 name: 0001
::0001::L'appareil servant à mesurer la vitesse du vent au sol s'appelle \:{
\t~une girouette.
\t~une rose des vents.
\t~un baromètre.
\t=un anémomètre.
}

// question: 2 name: 0002
::0002::L'unité de pression utilisée dans le système international et en aéronautique est \:{
\t=le pascal.
\t~le newton.
\t~le joule.
\t~le millimètre de mercure.
}"""
    quiz = GiftQuiz.parse(gift_text)
    assert len(quiz) == 2
    q = quiz._lst_questions[0]
    assert len(q) == 4
    assert q.is_correct_answer(3)
    q = quiz._lst_questions[1]
    assert len(q) == 4
    assert q.is_correct_answer(0)


def test_gift_parse_no_correct_answer():
    """Fix issue where a ZeroDivisionError: float division by zero was raised"""
    gift_text = """// question: 1 name: 0001
::0001::L'appareil servant à mesurer la vitesse du vent au sol s'appelle \:{
\t~une girouette.
\t~une rose des vents.
\t~un baromètre.
\t~un anémomètre.
}

// question: 2 name: 0002
::0002::L'unité de pression utilisée dans le système international et en aéronautique est \:{
\t~le pascal.
\t~le newton.
\t~le joule.
\t~le millimètre de mercure.
}"""
    quiz = GiftQuiz.parse(gift_text)
    assert len(quiz) == 2
    q = quiz._lst_questions[0]
    assert len(q) == 4
    q = quiz._lst_questions[1]
    assert len(q) == 4


def test_to_xml():
    quiz = GiftQuiz()
    q = GiftQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :", name="0001", comment="question: 1 name: 0001")
    q.append_distractor(GiftDistractor("une girouette.", 0))
    q.append_distractor(GiftDistractor("une rose des vents.", 0))
    q.append_distractor(GiftDistractor("un baromètre.", 0))
    q.append_distractor(GiftDistractor("un anémomètre.", 1))
    quiz.append(q)

    q = GiftQuestion("L'unité de pression utilisée dans le système international et en aéronautique est :", name="0002", comment="question: 2 name: 0002")
    q.append_distractor(GiftDistractor("le pascal.", 1))
    q.append_distractor(GiftDistractor("le newton.", 0))
    q.append_distractor(GiftDistractor("le joule.", 0))
    q.append_distractor(GiftDistractor("le millimètre de mercure.", 0))
    quiz.append(q)

    assert len(quiz) == 2

    xml_text = quiz.to_xml_moodle(category='$module$/Défaut pour BIA 2016 Météorologie et aérologie')

    expected_xml_text = """<?xml version="1.0" encoding="UTF-8"?>
<quiz>
  <question type="category">
    <category>
      <text>$module$/Défaut pour BIA 2016 Météorologie et aérologie</text>
    </category>
  </question>
</quiz>
<question type="multichoice">
  <name>
    <text>0001</text>
  </name>
  <questiontext>
    <text>L'appareil servant à mesurer la vitesse du vent au sol s'appelle :</text>
  </questiontext>
  <shuffleanswers>false</shuffleanswers>
  <answer fraction="0">
    <text>une girouette.</text>
  </answer>
  <answer fraction="0">
    <text>une rose des vents.</text>
  </answer>
  <answer fraction="0">
    <text>un baromètre.</text>
  </answer>
  <answer fraction="100">
    <text>un anémomètre.</text>
  </answer>
</question>
<question type="multichoice">
  <name>
    <text>0002</text>
  </name>
  <questiontext>
    <text>L'unité de pression utilisée dans le système international et en aéronautique est :</text>
  </questiontext>
  <shuffleanswers>false</shuffleanswers>
  <answer fraction="100">
    <text>le pascal.</text>
  </answer>
  <answer fraction="0">
    <text>le newton.</text>
  </answer>
  <answer fraction="0">
    <text>le joule.</text>
  </answer>
  <answer fraction="0">
    <text>le millimètre de mercure.</text>
  </answer>
</question>"""

    assert xml_text == expected_xml_text
