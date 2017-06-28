from lms_tools.aiken import AikenQuiz, AikenQuestion
from lms_tools.gift import GiftQuiz, GiftQuestion, GiftDistractor


def test_gift_question_to_string():
    q = GiftQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :", name="0001", comment="question: 1 name: 0001")
    q.append_distractor(GiftDistractor("une girouette.", 0))
    q.append_distractor(GiftDistractor("une rose des vents.", 0))
    q.append_distractor(GiftDistractor("un baromètre.", 0))
    q.append_distractor(GiftDistractor("un anémomètre.", 1))
    assert q.is_binary()
    assert q.is_correct_answer(3)
    assert not q.is_correct_answer(0)
    expected_gift_text = """// question: 1 name: 0001
::0001::L'appareil servant à mesurer la vitesse du vent au sol s'appelle \:{
\t~une girouette.
\t~une rose des vents.
\t~un baromètre.
\t=un anémomètre.
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
    aiken_txt = """L'appareil servant à mesurer la vitesse du vent au sol s'appelle :
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
    aiken_quiz = AikenQuiz.parse(aiken_txt)
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