from console_gfx import ConsoleGfx

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
