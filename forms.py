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


signup = """
<form method="post">
    <table>
        <tr>
            <td>Signup</td>
        </tr>
        <tr>
            <td>Username</td>
            <td><input type="text" name="username" value="%(username)s"></td>
            <td><div style="color: red">%(error_username)s</div></td>
        </tr>
        <tr>
            <td>Password</td>
            <td><input type="password" name="password" value=""></td>
            <td><div style="color: red">%(error_password)s</div></td>
        </tr>
        <tr>
            <td>Verify Password</td>
            <td><input type="password" name="verify" value=""></td>
            <td><div style="color: red">%(error_verify)s</div></td>
        </tr>
        <tr>
            <td>E-mail (optional)</td>
            <td><input type="text" name="email" value="%(email)s"></td>
            <td><div style="color: red">%(error_email)s</div></td>
        </tr>
    </table>
    <input type="submit">
</form>
"""
