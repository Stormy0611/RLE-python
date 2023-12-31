class ConsoleGfx:

    default_top = "═"
    default_up_left = "╔"
    default_up_right = "╗"
    default_start = "║"
    default_end = "║"
    default_bottom = "═"
    default_low_left = "╚"
    default_low_right = "╝"

    COLOR_RESET = '\033[0m'
    fg_palette = ['']*16
    em_palette = ['']*16
    ul_palette = ['']*16
    bg_palette = ['']*16

    for i in range(8):
        fg_palette[i] = '\033[3' + str(i) + 'm'
        fg_palette[i+8] = '\033[9' + str(i) + 'm'
        em_palette[i] = '\033[1;3' + str(i) + 'm'
        em_palette[i+8] = '\033[1;9' + str(i) + 'm'
        ul_palette[i] = '\033[4;3' + str(i) + 'm'
        ul_palette[i+8] = '\033[4;9' + str(i) + 'm'
        bg_palette[i] = '\033[4' + str(i) + 'm'
        bg_palette[i+8] = '\033[10' + str(i) + 'm'

    BLACK = 0
    RED = 1
    DARK_GREEN = 2
    GOLD = 3
    BLUE = 4
    GARNETT = 5
    ORANGE = 6
    LIGHT_GRAY = 7
    GRAY = 8
    PEACH = 9
    GREEN = 10
    BRIGHT_GOLD = 11
    CYAN = 12
    MAGENTA = 13
    BRIGHT_ORANGE = 14
    WHITE = 15

    CLEAR = MAGENTA
    TRANS_DISPLAY = BLACK

    test_rainbow = [16, 2,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    test_image = [14, 6,
        CLEAR, CLEAR, GREEN, GREEN, GREEN, CLEAR, CLEAR, CLEAR,
        CLEAR, CLEAR, CLEAR, GREEN, GREEN, CLEAR, CLEAR, GREEN,
        WHITE, BLACK, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN,
        GREEN, DARK_GREEN, GREEN, GREEN, GREEN, GREEN, GREEN,
        GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN,
        GREEN, GREEN, CLEAR, GREEN, GREEN, GREEN, GREEN, GREEN,
        GREEN, GREEN, GREEN, GREEN, BLACK, BLACK, BLACK, GREEN,
        CLEAR, GREEN, GREEN, GREEN, BLACK, BLACK, BLACK, BLACK,
        BLACK, BLACK, GREEN, GREEN, GREEN, CLEAR, CLEAR, CLEAR,
        GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN,
        CLEAR, CLEAR, CLEAR, CLEAR, CLEAR
        ]

    def display_image(image_data):
        ConsoleGfx.display_image2(image_data, ConsoleGfx.default_top, ConsoleGfx.default_up_left, ConsoleGfx.default_up_right, ConsoleGfx.default_start,
                          ConsoleGfx.default_end, ConsoleGfx.default_bottom, ConsoleGfx.default_low_left, ConsoleGfx.default_low_right)

    def display_image2(image_data, top, up_left, up_right, start, end, bottom, low_left, low_right):
        width = image_data[0]
        height = image_data[1]
        data_index = 2

        print(up_left, end='')
        for x_index in range(width):
            print(top, end='')
        print(up_right)

        for y_index in range(0, height, 2):
            output_str = start
            for x_index in range(width):
                output_color = image_data[data_index]
                output_str += ConsoleGfx.fg_palette[ConsoleGfx.TRANS_DISPLAY if output_color == ConsoleGfx.CLEAR else output_color]
                output_color = image_data[data_index + width] if y_index + 1 < height else ConsoleGfx.CLEAR
                output_str += ConsoleGfx.bg_palette[ConsoleGfx.TRANS_DISPLAY if output_color == ConsoleGfx.CLEAR else output_color]
                output_str += '▀'
                data_index += 1
            data_index += width
            print(output_str + ConsoleGfx.COLOR_RESET + end)

        print(low_left, end='')
        for x_index in range(width):
            print(bottom, end='')
        print(low_right)

    def load_file(filename):
        file_data = []
        with open(filename, 'rb') as my_file:

            contents = my_file.read()

            for c in contents:
                file_data += [c]

            my_file.close()

        return file_data

    def to_hex_string(data):
        hex_list = []
        hex_list.extend([hex(data[0])[2:].zfill(2), hex(data[1])[2:].zfill(2)])
        for value in data[2:]:
            hex_list.append(hex(value)[2:].zfill(1))
        return ''.join(hex_list)

    def count_runs(flat_data):
        temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        count = 0

        for value in flat_data:
            temp[value] = 1
        
        for tp in temp:
            count = count + tp
            
        return count

    def encode_rle(flat_data):
        encoded = []
        encoded.extend([flat_data[0], flat_data[1]])
        run_length = 1
        prev = flat_data[2]
        
        for value in flat_data[3:]:
            if value == prev:
                run_length += 1
            else:
                encoded.extend([run_length, prev])
                run_length = 1
                prev = value
            
        encoded.extend([run_length, prev])
        return encoded

    def get_decoded_length(rle_data):
        return sum(rle_data[0::2])

    def decode_rle(rle_data):
        decoded = []
        decoded.extend([rle_data[0], rle_data[1]])
        
        for i in range(2, len(rle_data), 2):
            run_length = rle_data[i]
            value = rle_data[i+1]
            
            decoded.extend([value] * run_length)
            
        return decoded

    def string_to_data(data_string):
        values = []
        values.extend([int(data_string[0:2], 16), int(data_string[2:4], 16)])
        for i in range(4, len(data_string)):
            values.append(int(data_string[i], 16))

        return values

    def to_rle_string(rle_data):
        rle_str = f"{rle_data[0]}:{rle_data[1]}"
        
        for i in range(2, len(rle_data), 2):
            rle_str += ":" + str(rle_data[i]) + hex(rle_data[i+1])[2:].zfill(1)
            
        return rle_str
    
    def string_to_rle(rle_string):
        values = []
        items = rle_string.split(':')
        values.extend([int(items[0]), int(items[1])])
        for value in items[2:]:
            values.extend([int(value[:-1]), int(value[-1], 16)])
        return values

image_data = None
width = 40
height = 10

def display_menu():
  print("\nRLE Menu\n--------")  
  print("0. Exit")
  print("1. Load File")
  print("2. Load Test Image")
  print("3. Read RLE String")
  print("4. Read RLE Hex String")
  print("5. Read Data Hex String")
  print("6. Display Image")
  print("7. Display RLE String")
  print("8. Display Hex RLE Data")
  print("9. Display Hex Flat Data")

def load_file():
  global image_data
  filename = input("Enter name of file to load: ")
  image_data = ConsoleGfx.load_file(filename)

def load_test_image():
  global image_data
  image_data = ConsoleGfx.test_image
  print("Test image data loaded.")

def read_rle_string():

  global image_data
  
  rle_str = input("Enter an RLE string to be decoded: ")

  # Decode RLE string into values
  values = ConsoleGfx.string_to_rle(rle_str)  

  # Decode values into pixel data
  decoded = ConsoleGfx.decode_rle(values)

  image_data = decoded

def read_rle_hex_string():
  global image_data
  hex_str = input("Enter the hex string holding RLE data: ")
  image_data = ConsoleGfx.decode_rle(ConsoleGfx.string_to_data(hex_str))

def read_flat_data_hex_string():
  global image_data
  hex_str = input("Enter the hex string holding flat data: ")
  image_data = ConsoleGfx.string_to_data(hex_str)

def display_image():
  ConsoleGfx.display_image(image_data)

def display_rle_string():
  print("RLE representation:", ConsoleGfx.to_rle_string(ConsoleGfx.encode_rle(image_data)))

def display_rle_hex_data():
  print("RLE hex values:", ConsoleGfx.to_hex_string(ConsoleGfx.encode_rle(image_data)))

def display_flat_hex_data():
  print("Flat hex values:", ConsoleGfx.to_hex_string(image_data))

def main():

  global image_data
  image_data = ConsoleGfx.test_rainbow
  
  print("Welcome to the RLE image encoder!")
  ConsoleGfx.display_image(ConsoleGfx.test_rainbow)
  
  while True:
    display_menu()
    option = input("Select a Menu Option: ")
    try:
      if option == "0":
        break
        
      elif option == "1":
        load_file()
        
      elif option == "2":
        load_test_image()
        
      elif option == "3":
        read_rle_string()
        
      elif option == "4":
        read_rle_hex_string()
        
      elif option == "5":
        read_flat_data_hex_string()
        
      elif option == "6":
        display_image()
        
      elif option == "7":
        display_rle_string()
        
      elif option == "8":
        display_rle_hex_data()
        
      elif option == "9":
        display_flat_hex_data()
        
      else:
        print("Invalid option. Please try again.")
    except Exception as err:
      print(err)

if __name__ == '__main__':
    main()
