from lms_tools.aiken import AikenQuiz, AikenQuestion
from lms_tools.gift import GiftQuiz, GiftQuestion, GiftDistractor


def test_aiken_question():
    stem = "L'appareil servant à mesurer la vitesse du vent au sol s'appelle :"
    distractors = ["une girouette.", "une rose des vents.", "un baromètre.", "un anémomètre."]
    correct_answer = 3
    question = AikenQuestion(stem, distractors, correct_answer)
    assert question.stem == stem
    assert question.distractors == distractors
    assert question.correct_answer == correct_answer


def test_aiken_question_stream():
    stem = "L'appareil servant à mesurer la vitesse du vent au sol s'appelle :"
    distractors = ["une girouette.", "une rose des vents.", "un baromètre.", "un anémomètre."]
    correct_answer = 3

    question = AikenQuestion()
    question.append_stem(stem)
    question.append_distractor(distractors[0])
    question.append_distractor(distractors[1])
    question.append_distractor(distractors[2])
    question.append_distractor(distractors[3])
    question.set_correct_answer(correct_answer)

    assert question.stem == stem
    assert question.distractors == distractors
    assert question.correct_answer == correct_answer


def test_aiken_question_to_string():
    q = AikenQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :",
                      ["une girouette.", "une rose des vents.", "un baromètre.", "un anémomètre."], 3)
    text = """L'appareil servant à mesurer la vitesse du vent au sol s'appelle :
A) une girouette.
B) une rose des vents.
C) un baromètre.
D) un anémomètre.
ANSWER: D"""
    assert q.to_string() == text


def test_aiken_question_parse():
    s = """L'appareil servant à mesurer la vitesse du vent au sol s'appelle :
A) une girouette.
B) une rose des vents.
C) un baromètre.
D) un anémomètre.
ANSWER: D"""
    question = AikenQuestion.parse(s)
    assert question.stem == "L'appareil servant à mesurer la vitesse du vent au sol s'appelle :"


def test_aiken_quiz():
    q1 = AikenQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :",
                       ["une girouette.", "une rose des vents.", "un baromètre.", "un anémomètre."], 3)
    q2 = AikenQuestion("L'unité de pression utilisée dans le système international et en aéronautique est :",
                       ["le pascal.", "le newton.", "le joule.", "le millimètre de mercure."], 0)
    quiz = AikenQuiz([q1, q2])
    assert len(quiz) == 2


def test_aiken_quiz_stream():
    quiz = AikenQuiz()
    q1 = AikenQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :",
                       ["une girouette.", "une rose des vents.", "un baromètre.", "un anémomètre."], 3)
    quiz.append(q1)
    q2 = AikenQuestion("L'unité de pression utilisée dans le système international et en aéronautique est :",
                       ["le pascal.", "le newton.", "le joule.", "le millimètre de mercure."], 0)
    quiz.append(q2)
    assert len(quiz) == 2


def test_aiken_quiz_to_string():
    q1 = AikenQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :",
                       ["une girouette.", "une rose des vents.", "un baromètre.", "un anémomètre."], 3)
    q2 = AikenQuestion("L'unité de pression utilisée dans le système international et en aéronautique est :",
                       ["le pascal.", "le newton.", "le joule.", "le millimètre de mercure."], 0)
    quiz = AikenQuiz([q1, q2])
    text = """L'appareil servant à mesurer la vitesse du vent au sol s'appelle :
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
    assert quiz.to_string() == text


def test_aiken_quiz_parse():
    text = """L'appareil servant à mesurer la vitesse du vent au sol s'appelle :
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
    quiz = AikenQuiz.parse(text)
    assert len(quiz) == 2
    assert quiz.to_string() == text


def test_aiken_question_from_gift_question():
    stem = "L'appareil servant à mesurer la vitesse du vent au sol s'appelle :"
    q = GiftQuestion(stem, name="0001")
    q.append_distractor(GiftDistractor("une girouette.", 0))
    q.append_distractor(GiftDistractor("une rose des vents.", 0))
    q.append_distractor(GiftDistractor("un baromètre.", 0))
    q.append_distractor(GiftDistractor("un anémomètre.", 1))
    assert q.is_binary()
    aiken_question = AikenQuestion.from_gift(q)
    assert isinstance(aiken_question, AikenQuestion)
    assert q.stem == aiken_question.stem
    assert len(aiken_question) == len(q)
    assert aiken_question.is_correct_answer(3)


def test_aiken_quiz_from_gift_quiz():
    gift_quiz = GiftQuiz()

    q = GiftQuestion("L'appareil servant à mesurer la vitesse du vent au sol s'appelle :", name="0001", comment="question: 1 name: 0001")
    q.append_distractor(GiftDistractor("une girouette.", 0))
    q.append_distractor(GiftDistractor("une rose des vents.", 0))
    q.append_distractor(GiftDistractor("un baromètre.", 0))
    q.append_distractor(GiftDistractor("un anémomètre.", 1))
    gift_quiz.append(q)

    q = GiftQuestion("L'unité de pression utilisée dans le système international et en aéronautique est :", name="0002", comment="question: 2 name: 0002")
    q.append_distractor(GiftDistractor("le pascal.", 1))
    q.append_distractor(GiftDistractor("le newton.", 0))
    q.append_distractor(GiftDistractor("le joule.", 0))
    q.append_distractor(GiftDistractor("le millimètre de mercure.", 0))
    gift_quiz.append(q)

    aiken_quiz = AikenQuiz.from_gift(gift_quiz)

    assert len(aiken_quiz) == len(gift_quiz)


def test_aiken_quiz_join():
    text1 = """L'appareil servant à mesurer la vitesse du vent au sol s'appelle :
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
    quiz1 = AikenQuiz.parse(text1)

    text2 = """En vol en palier stabilisé :
A) la portance équilibre le poids.
B) la portance équilibre la traînée.
C) la portance équilibre la résultante aérodynamique.
D) la portance équilibre la force de propulsion.
ANSWER: A

Le vent relatif :
A) est la composante du vent réel parallèle à la trajectoire.
B) est parallèle à la trajectoire, et de même sens que le déplacement de l'avion.
C) est parallèle à la trajectoire, mais de sens opposé au déplacement de l'avion.
D) est la composante du vent réel perpendiculaire à la trajectoire.
ANSWER: C"""
    quiz2 = AikenQuiz.parse(text2)
    quiz_result = AikenQuiz.join([quiz1, quiz2])

    expected_text = """L'appareil servant à mesurer la vitesse du vent au sol s'appelle :
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
ANSWER: A

En vol en palier stabilisé :
A) la portance équilibre le poids.
B) la portance équilibre la traînée.
C) la portance équilibre la résultante aérodynamique.
D) la portance équilibre la force de propulsion.
ANSWER: A

Le vent relatif :
A) est la composante du vent réel parallèle à la trajectoire.
B) est parallèle à la trajectoire, et de même sens que le déplacement de l'avion.
C) est parallèle à la trajectoire, mais de sens opposé au déplacement de l'avion.
D) est la composante du vent réel perpendiculaire à la trajectoire.
ANSWER: C"""
    assert len(quiz_result) == 4
    assert quiz_result.to_string() == expected_text
