birthday = """
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <input type="submit">
</form>
"""


rot13 = """
<form method="post">
    Enter some text to ROT13:
    <br>
    <textarea name=text
              style="height: 100px; width: 400px;">%(text)s</textarea>
    <br>
    <input type="submit">
</form>
"""
