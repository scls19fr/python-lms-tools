from enum import Enum


AikenParserState = Enum("AikenParserState", "START STEM DISTRACTORS CORRECT_ANSWER")

DISTRACTORS_PATTERN = "^([A-Za-z])[\)|.]\s*(.*)$"
CORRECT_ANSWER_PATTERN = "^ANSWER:\s*(.*)$"
