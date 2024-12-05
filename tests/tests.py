from src.Edexcel_Pseudocode import translation

# The following pseudocode is from the 2024 June CS paper 1
pseudocode = """
SET arrival TO [-2, 1, 5, 0, -3, 4, 1]

SET early to 0
SET late to 0
SET index to 0

WHILE NOT (arrival > LENGTH(arrival)) DO

    IF arrival[index] >= 0 THEN
        SET late TO arrival[index]
    ELSE
        IF arrival[index] < 0 THEN
            SET early TO early + 1
        END IF

        SET index TO index + 1

END WHILE

# string concatenation will be temporarily changed to + instead of &
SEND "Trains early:    " + early TO DISPLAY
SEND "Trains on time:    " + (late + early) TO DISPLAY
SEND "Trains late:    " + late TO DISPLAY
"""

pseudocode = "SEND \"hello, world\n\" TO DISPLAY"

def test_output(capfd):
    translate = translation.Translation(pseudocode)
    translate.transpile()
    translate.output("transpiled.py")
    output, _error = capfd.readouterr()
    assert output == "hello, world\n"