#hastily written script to generate emojicode to print out text

smile = '😃'
move_left = '👈'
move_right = '👉'
sun = '🌞'
moon = '🌝'
kissy_face = '😘'

text = input("Enter Text: ")


code = ''
for character in text:
    for index, i in enumerate(range(ord(character))):
        if index % 10 == 0:
            code += '\n'
        code += smile
    code += move_right + '\n'

code += move_left + sun + move_left + moon

code += move_right + sun + kissy_face + move_right + moon

code += sun + move_left + moon

print(code)

