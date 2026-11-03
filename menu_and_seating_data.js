const fs = require('fs');
const path = require('path');

const MENU_ITEMS = [
  {
    "id": "TT-001",
    "name": "Chilli Paneer",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Starter",
    "isAvailable": true
  },
  {
    "id": "TT-002",
    "name": "Paneer 65",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Starter",
    "isAvailable": true
  },
  {
    "id": "TT-003",
    "name": "Paneer 555",
    "category": "Veg Starters",
    "price": 250,
    "isVeg": true,
    "tag": "Special",
    "isAvailable": true
  },
  {
    "id": "TT-004",
    "name": "Chilli Mushroom",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Starter",
    "isAvailable": true
  },
  {
    "id": "TT-005",
    "name": "Mushroom 65",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Starter",
    "isAvailable": true
  },
  {
    "id": "TT-006",
    "name": "Pepper Mushroom",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Spicy",
    "isAvailable": true
  },
  {
    "id": "TT-007",
    "name": "Paneer Pakoda",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Crispy",
    "isAvailable": true
  },
  {
    "id": "TT-008",
    "name": "Mushroom Pakoda",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Crispy",
    "isAvailable": true
  },
  {
    "id": "TT-009",
    "name": "Paneer Manchuria",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Indo-Chinese",
    "isAvailable": true
  },
  {
    "id": "TT-010",
    "name": "Mushroom Manchuria",
    "category": "Veg Starters",
    "price": 230,
    "isVeg": true,
    "tag": "Indo-Chinese",
    "isAvailable": true
  },
  {
    "id": "TT-011",
    "name": "Tandoori Chicken (1/2)",
    "category": "Kebabs",
    "price": 250,
    "isVeg": false,
    "tag": "Half",
    "isAvailable": true
  },
  {
    "id": "TT-012",
    "name": "Tandoori Chicken (Full)",
    "category": "Kebabs",
    "price": 450,
    "isVeg": false,
    "tag": "Full",
    "isAvailable": true
  },
  {
    "id": "TT-013",
    "name": "Chicken Tikka",
    "category": "Kebabs",
    "price": 230,
    "isVeg": false,
    "tag": "Tandoor",
    "isAvailable": true
  },
  {
    "id": "TT-014",
    "name": "Hariyali Tikka",
    "category": "Kebabs",
    "price": 250,
    "isVeg": false,
    "tag": "Mint Herbal",
    "isAvailable": true
  },
  {
    "id": "TT-015",
    "name": "Kalmi Kebab",
    "category": "Kebabs",
    "price": 250,
    "isVeg": false,
    "tag": "Tandoor",
    "isAvailable": true
  },
  {
    "id": "TT-016",
    "name": "Afghani Kebab",
    "category": "Kebabs",
    "price": 250,
    "isVeg": false,
    "tag": "Creamy",
    "isAvailable": true
  },
  {
    "id": "TT-017",
    "name": "Tangadi Kebab",
    "category": "Kebabs",
    "price": 250,
    "isVeg": false,
    "tag": "Drumstick",
    "isAvailable": true
  },
  {
    "id": "TT-018",
    "name": "Reshmi Kebab",
    "category": "Kebabs",
    "price": 250,
    "isVeg": false,
    "tag": "Silky Mild",
    "isAvailable": true
  },
  {
    "id": "TT-019",
    "name": "Malai Tikka",
    "category": "Kebabs",
    "price": 300,
    "isVeg": false,
    "tag": "Rich Cream",
    "isAvailable": true
  },
  {
    "id": "TT-020",
    "name": "Full Joint",
    "category": "Kebabs",
    "price": 150,
    "isVeg": false,
    "tag": "Special",
    "isAvailable": true
  },
  {
    "id": "TT-021",
    "name": "Chilly Chicken",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Starter",
    "isAvailable": true
  },
  {
    "id": "TT-022",
    "name": "Chicken 65",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Popular",
    "isAvailable": true
  },
  {
    "id": "TT-023",
    "name": "Chicken Manchurian",
    "category": "Non-Veg Starters",
    "price": 230,
    "isVeg": false,
    "tag": "Indo-Chinese",
    "isAvailable": true
  },
  {
    "id": "TT-024",
    "name": "Chicken 555",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Chef Special",
    "isAvailable": true
  },
  {
    "id": "TT-025",
    "name": "Chicken Majestic",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Curry Leaf",
    "isAvailable": true
  },
  {
    "id": "TT-026",
    "name": "Garlic Chicken",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Garlic Toss",
    "isAvailable": true
  },
  {
    "id": "TT-027",
    "name": "Pepper Chicken",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Black Pepper",
    "isAvailable": true
  },
  {
    "id": "TT-028",
    "name": "Dragon Chicken",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Hot & Sweet",
    "isAvailable": true
  },
  {
    "id": "TT-029",
    "name": "Lollipop Starter (5 pcs)",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "5 Pcs",
    "isAvailable": true
  },
  {
    "id": "TT-030",
    "name": "Wings Starter (4 pcs)",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "4 Pcs",
    "isAvailable": true
  },
  {
    "id": "TT-031",
    "name": "Joint Starter (4 pcs)",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "4 Pcs",
    "isAvailable": true
  },
  {
    "id": "TT-032",
    "name": "Lemon Chicken",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Tangy",
    "isAvailable": true
  },
  {
    "id": "TT-033",
    "name": "Chilli Prawn",
    "category": "Non-Veg Starters",
    "price": 280,
    "isVeg": false,
    "tag": "Seafood",
    "isAvailable": true
  },
  {
    "id": "TT-034",
    "name": "Prawn 65",
    "category": "Non-Veg Starters",
    "price": 280,
    "isVeg": false,
    "tag": "Crispy Seafood",
    "isAvailable": true
  },
  {
    "id": "TT-035",
    "name": "Pepper Prawn",
    "category": "Non-Veg Starters",
    "price": 280,
    "isVeg": false,
    "tag": "Black Pepper",
    "isAvailable": true
  },
  {
    "id": "TT-036",
    "name": "Loose Prawn",
    "category": "Non-Veg Starters",
    "price": 280,
    "isVeg": false,
    "tag": "Special Fry",
    "isAvailable": true
  },
  {
    "id": "TT-037",
    "name": "Prawn Manchuria",
    "category": "Non-Veg Starters",
    "price": 250,
    "isVeg": false,
    "tag": "Indo-Chinese",
    "isAvailable": true
  },
  {
    "id": "TT-038",
    "name": "Talking Tables Special",
    "category": "Non-Veg Starters",
    "price": 300,
    "isVeg": false,
    "tag": "House Signature",
    "isAvailable": true
  },
  {
    "id": "TT-039",
    "name": "Tomato Curry",
    "category": "Main Course-Veg",
    "price": 150,
    "isVeg": true,
    "tag": "Curry",
    "isAvailable": true
  },
  {
    "id": "TT-040",
    "name": "Paneer Curry",
    "category": "Main Course-Veg",
    "price": 200,
    "isVeg": true,
    "tag": "Curry",
    "isAvailable": true
  },
  {
    "id": "TT-041",
    "name": "Paneer Butter Masala",
    "category": "Main Course-Veg",
    "price": 220,
    "isVeg": true,
    "tag": "Bestseller",
    "isAvailable": true
  },
  {
    "id": "TT-042",
    "name": "Kaju Curry",
    "category": "Main Course-Veg",
    "price": 200,
    "isVeg": true,
    "tag": "Cashew",
    "isAvailable": true
  },
  {
    "id": "TT-043",
    "name": "Kaju Tomato Curry",
    "category": "Main Course-Veg",
    "price": 220,
    "isVeg": true,
    "tag": "Rich Gravy",
    "isAvailable": true
  },
  {
    "id": "TT-044",
    "name": "Kaju Paneer Curry",
    "category": "Main Course-Veg",
    "price": 220,
    "isVeg": true,
    "tag": "Deluxe",
    "isAvailable": true
  },
  {
    "id": "TT-045",
    "name": "Mushroom Curry",
    "category": "Main Course-Veg",
    "price": 200,
    "isVeg": true,
    "tag": "Curry",
    "isAvailable": true
  },
  {
    "id": "TT-046",
    "name": "Mushroom Masala",
    "category": "Main Course-Veg",
    "price": 200,
    "isVeg": true,
    "tag": "Masala",
    "isAvailable": true
  },
  {
    "id": "TT-047",
    "name": "Methi Chaman Curry",
    "category": "Main Course-Veg",
    "price": 200,
    "isVeg": true,
    "tag": "Fenugreek",
    "isAvailable": true
  },
  {
    "id": "TT-048",
    "name": "Kadai Paneer",
    "category": "Main Course-Veg",
    "price": 200,
    "isVeg": true,
    "tag": "Wok Tossed",
    "isAvailable": true
  },
  {
    "id": "TT-049",
    "name": "Kadai Mushroom",
    "category": "Main Course-Veg",
    "price": 200,
    "isVeg": true,
    "tag": "Wok Tossed",
    "isAvailable": true
  },
  {
    "id": "TT-050",
    "name": "Kadai Kaju",
    "category": "Main Course-Veg",
    "price": 200,
    "isVeg": true,
    "tag": "Wok Tossed",
    "isAvailable": true
  },
  {
    "id": "TT-051",
    "name": "Plain Naan",
    "category": "Breads",
    "price": 30,
    "isVeg": true,
    "tag": "Clay Oven",
    "isAvailable": true
  },
  {
    "id": "TT-052",
    "name": "Butter Naan",
    "category": "Breads",
    "price": 40,
    "isVeg": true,
    "tag": "Popular",
    "isAvailable": true
  },
  {
    "id": "TT-053",
    "name": "Garlic Naan",
    "category": "Breads",
    "price": 50,
    "isVeg": true,
    "tag": "Fresh Garlic",
    "isAvailable": true
  },
  {
    "id": "TT-054",
    "name": "Plain Kulcha",
    "category": "Breads",
    "price": 50,
    "isVeg": true,
    "tag": "Tandoor",
    "isAvailable": true
  },
  {
    "id": "TT-055",
    "name": "Masala Kulcha",
    "category": "Breads",
    "price": 60,
    "isVeg": true,
    "tag": "Stuffed",
    "isAvailable": true
  },
  {
    "id": "TT-056",
    "name": "Tandoori Roti",
    "category": "Breads",
    "price": 25,
    "isVeg": true,
    "tag": "Wheat",
    "isAvailable": true
  },
  {
    "id": "TT-057",
    "name": "Butter Roti",
    "category": "Breads",
    "price": 35,
    "isVeg": true,
    "tag": "Wheat Butter",
    "isAvailable": true
  },
  {
    "id": "TT-058",
    "name": "Rumali Roti",
    "category": "Breads",
    "price": 30,
    "isVeg": true,
    "tag": "Thin Handkerchief",
    "isAvailable": true
  },
  {
    "id": "TT-059",
    "name": "Chicken Bone Curry",
    "category": "Non-Veg Curries",
    "price": 150,
    "isVeg": false,
    "tag": "Traditional",
    "isAvailable": true
  },
  {
    "id": "TT-060",
    "name": "Chicken Boneless Curry",
    "category": "Non-Veg Curries",
    "price": 230,
    "isVeg": false,
    "tag": "Boneless",
    "isAvailable": true
  },
  {
    "id": "TT-061",
    "name": "Mughlai Curry",
    "category": "Non-Veg Curries",
    "price": 250,
    "isVeg": false,
    "tag": "Egg Dropped",
    "isAvailable": true
  },
  {
    "id": "TT-062",
    "name": "Kadai Chicken Bone",
    "category": "Non-Veg Curries",
    "price": 200,
    "isVeg": false,
    "tag": "Bell Pepper",
    "isAvailable": true
  },
  {
    "id": "TT-063",
    "name": "Kadai Chicken Boneless",
    "category": "Non-Veg Curries",
    "price": 250,
    "isVeg": false,
    "tag": "Kadai Gravy",
    "isAvailable": true
  },
  {
    "id": "TT-064",
    "name": "Lollipop Curry (5 pcs)",
    "category": "Non-Veg Curries",
    "price": 250,
    "isVeg": false,
    "tag": "5 Pcs Gravy",
    "isAvailable": true
  },
  {
    "id": "TT-065",
    "name": "Butter Chicken",
    "category": "Non-Veg Curries",
    "price": 250,
    "isVeg": false,
    "tag": "Creamy Tomato",
    "isAvailable": true
  },
  {
    "id": "TT-066",
    "name": "Chicken Tikka Masala",
    "category": "Non-Veg Curries",
    "price": 250,
    "isVeg": false,
    "tag": "Smoked Tikka",
    "isAvailable": true
  },
  {
    "id": "TT-067",
    "name": "Punjabi Chicken",
    "category": "Non-Veg Curries",
    "price": 250,
    "isVeg": false,
    "tag": "Rich Masala",
    "isAvailable": true
  },
  {
    "id": "TT-068",
    "name": "Methi Chicken",
    "category": "Non-Veg Curries",
    "price": 250,
    "isVeg": false,
    "tag": "Fenugreek",
    "isAvailable": true
  },
  {
    "id": "TT-069",
    "name": "Tandoori Chicken Masala",
    "category": "Non-Veg Curries",
    "price": 280,
    "isVeg": false,
    "tag": "Charcoal Flavored",
    "isAvailable": true
  },
  {
    "id": "TT-070",
    "name": "Chicken Maharaja",
    "category": "Non-Veg Curries",
    "price": 280,
    "isVeg": false,
    "tag": "Royal Spiced",
    "isAvailable": true
  },
  {
    "id": "TT-071",
    "name": "Prawn Curry",
    "category": "Non-Veg Curries",
    "price": 280,
    "isVeg": false,
    "tag": "Coastal Gravy",
    "isAvailable": true
  },
  {
    "id": "TT-072",
    "name": "Prawn Masala",
    "category": "Non-Veg Curries",
    "price": 280,
    "isVeg": false,
    "tag": "Thick Masala",
    "isAvailable": true
  },
  {
    "id": "TT-073",
    "name": "Prawn Butter Masala",
    "category": "Non-Veg Curries",
    "price": 300,
    "isVeg": false,
    "tag": "Butter Rich",
    "isAvailable": true
  },
  {
    "id": "TT-074",
    "name": "Kadai Prawn",
    "category": "Non-Veg Curries",
    "price": 280,
    "isVeg": false,
    "tag": "Spiced Prawn",
    "isAvailable": true
  },
  {
    "id": "TT-075",
    "name": "Chicken Kheema Masala",
    "category": "Non-Veg Curries",
    "price": 250,
    "isVeg": false,
    "tag": "Minced Chicken",
    "isAvailable": true
  },
  {
    "id": "TT-076",
    "name": "Egg Kheema Masala",
    "category": "Non-Veg Curries",
    "price": 180,
    "isVeg": false,
    "tag": "Egg Scramble",
    "isAvailable": true
  },
  {
    "id": "TT-077",
    "name": "Egg Masala",
    "category": "Non-Veg Curries",
    "price": 180,
    "isVeg": false,
    "tag": "Boiled Egg (2)",
    "isAvailable": true
  },
  {
    "id": "TT-078",
    "name": "Mutton Fry",
    "category": "Non-Veg Curries",
    "price": 350,
    "isVeg": false,
    "tag": "Tender Lamb",
    "isAvailable": true
  },
  {
    "id": "TT-079",
    "name": "Mutton Curry",
    "category": "Non-Veg Curries",
    "price": 350,
    "isVeg": false,
    "tag": "Homestyle Gravy",
    "isAvailable": true
  },
  {
    "id": "TT-080",
    "name": "Mutton Rogan Josh",
    "category": "Non-Veg Curries",
    "price": 350,
    "isVeg": false,
    "tag": "Kashmiri Spiced",
    "isAvailable": true
  },
  {
    "id": "TT-081",
    "name": "Mutton Masala",
    "category": "Non-Veg Curries",
    "price": 350,
    "isVeg": false,
    "tag": "Rich Gravy",
    "isAvailable": true
  },
  {
    "id": "TT-082",
    "name": "Kaju Biryani",
    "category": "Veg Biryani's",
    "price": 220,
    "isVeg": true,
    "tag": "Ghee Cashew",
    "isAvailable": true
  },
  {
    "id": "TT-083",
    "name": "Mushroom Biryani",
    "category": "Veg Biryani's",
    "price": 200,
    "isVeg": true,
    "tag": "Fresh Mushroom",
    "isAvailable": true
  },
  {
    "id": "TT-084",
    "name": "Paneer Biryani",
    "category": "Veg Biryani's",
    "price": 220,
    "isVeg": true,
    "tag": "Cottage Cheese",
    "isAvailable": true
  },
  {
    "id": "TT-085",
    "name": "Mixed Veg Biryani",
    "category": "Veg Biryani's",
    "price": 250,
    "isVeg": true,
    "tag": "Farm Fresh",
    "isAvailable": true
  },
  {
    "id": "TT-086",
    "name": "Ghee Pulav",
    "category": "Veg Biryani's",
    "price": 180,
    "isVeg": true,
    "tag": "Pure Cow Ghee",
    "isAvailable": true
  },
  {
    "id": "TT-087",
    "name": "Dum Biryani",
    "category": "Non-Veg Biryani's",
    "price": 150,
    "isVeg": false,
    "tag": "Classic Hyderabadi",
    "isAvailable": true
  },
  {
    "id": "TT-088",
    "name": "Fry Biryani",
    "category": "Non-Veg Biryani's",
    "price": 220,
    "isVeg": false,
    "tag": "Spicy Roast Chicken",
    "isAvailable": true
  },
  {
    "id": "TT-089",
    "name": "Lollipop Biryani (3 pcs)",
    "category": "Non-Veg Biryani's",
    "price": 250,
    "isVeg": false,
    "tag": "3 Pcs Lollipop",
    "isAvailable": true
  },
  {
    "id": "TT-090",
    "name": "Wings Biryani (3 pcs)",
    "category": "Non-Veg Biryani's",
    "price": 250,
    "isVeg": false,
    "tag": "3 Pcs Wings",
    "isAvailable": true
  },
  {
    "id": "TT-091",
    "name": "Joint Biryani (3 pcs)",
    "category": "Non-Veg Biryani's",
    "price": 300,
    "isVeg": false,
    "tag": "3 Pcs Leg Joint",
    "isAvailable": true
  },
  {
    "id": "TT-092",
    "name": "Boneless Biryani",
    "category": "Non-Veg Biryani's",
    "price": 280,
    "isVeg": false,
    "tag": "Tender Boneless",
    "isAvailable": true
  },
  {
    "id": "TT-093",
    "name": "Mughlai Biryani",
    "category": "Non-Veg Biryani's",
    "price": 300,
    "isVeg": false,
    "tag": "Royal Egg Glazed",
    "isAvailable": true
  },
  {
    "id": "TT-094",
    "name": "Tandoori Chicken Biryani",
    "category": "Non-Veg Biryani's",
    "price": 250,
    "isVeg": false,
    "tag": "Smoked Tandoori",
    "isAvailable": true
  },
  {
    "id": "TT-095",
    "name": "Tandoori Tangadi Biryani",
    "category": "Non-Veg Biryani's",
    "price": 280,
    "isVeg": false,
    "tag": "Roasted Drumstick",
    "isAvailable": true
  },
  {
    "id": "TT-096",
    "name": "Tandoori Tikka Biryani",
    "category": "Non-Veg Biryani's",
    "price": 250,
    "isVeg": false,
    "tag": "Tandoor Tikka",
    "isAvailable": true
  },
  {
    "id": "TT-097",
    "name": "Chicken Kheema Biryani",
    "category": "Non-Veg Biryani's",
    "price": 300,
    "isVeg": false,
    "tag": "Spiced Minced",
    "isAvailable": true
  },
  {
    "id": "TT-098",
    "name": "Prawns Fry Biryani",
    "category": "Non-Veg Biryani's",
    "price": 300,
    "isVeg": false,
    "tag": "Crispy Prawn",
    "isAvailable": true
  },
  {
    "id": "TT-099",
    "name": "Prawns Curry Biryani",
    "category": "Non-Veg Biryani's",
    "price": 300,
    "isVeg": false,
    "tag": "Juicy Prawn",
    "isAvailable": true
  },
  {
    "id": "TT-100",
    "name": "Mutton Fry Biryani",
    "category": "Non-Veg Biryani's",
    "price": 300,
    "isVeg": false,
    "tag": "Roast Tender Lamb",
    "isAvailable": true
  },
  {
    "id": "TT-101",
    "name": "Mutton Curry Biryani",
    "category": "Non-Veg Biryani's",
    "price": 320,
    "isVeg": false,
    "tag": "Juicy Lamb",
    "isAvailable": true
  },
  {
    "id": "TT-102",
    "name": "Egg Biryani",
    "category": "Non-Veg Biryani's",
    "price": 150,
    "isVeg": false,
    "tag": "Double Boiled Egg",
    "isAvailable": true
  },
  {
    "id": "TT-103",
    "name": "Egg Kheema Biryani",
    "category": "Non-Veg Biryani's",
    "price": 180,
    "isVeg": false,
    "tag": "Egg Minced",
    "isAvailable": true
  },
  {
    "id": "TT-104",
    "name": "Veg Fried Rice",
    "category": "Veg Rice Items",
    "price": 120,
    "isVeg": true,
    "tag": "Wok Tossed",
    "isAvailable": true
  },
  {
    "id": "TT-105",
    "name": "Jeera Rice",
    "category": "Veg Rice Items",
    "price": 130,
    "isVeg": true,
    "tag": "Cumin Ghee",
    "isAvailable": true
  },
  {
    "id": "TT-106",
    "name": "Mushroom Fried Rice",
    "category": "Veg Rice Items",
    "price": 140,
    "isVeg": true,
    "tag": "Wok Tossed",
    "isAvailable": true
  },
  {
    "id": "TT-107",
    "name": "Paneer Fried Rice",
    "category": "Veg Rice Items",
    "price": 150,
    "isVeg": true,
    "tag": "Cottage Cheese",
    "isAvailable": true
  },
  {
    "id": "TT-108",
    "name": "Kaju Fried Rice",
    "category": "Veg Rice Items",
    "price": 150,
    "isVeg": true,
    "tag": "Cashew Rice",
    "isAvailable": true
  },
  {
    "id": "TT-109",
    "name": "Special Mixed Fried Rice",
    "category": "Veg Rice Items",
    "price": 180,
    "isVeg": true,
    "tag": "Chef Special",
    "isAvailable": true
  },
  {
    "id": "TT-110",
    "name": "Chicken Fried Rice",
    "category": "Non-Veg Rice Items",
    "price": 150,
    "isVeg": false,
    "tag": "Popular",
    "isAvailable": true
  },
  {
    "id": "TT-111",
    "name": "Egg Fried Rice",
    "category": "Non-Veg Rice Items",
    "price": 130,
    "isVeg": false,
    "tag": "Fresh Egg",
    "isAvailable": true
  },
  {
    "id": "TT-112",
    "name": "Double Egg Fried Rice",
    "category": "Non-Veg Rice Items",
    "price": 140,
    "isVeg": false,
    "tag": "Extra Egg",
    "isAvailable": true
  },
  {
    "id": "TT-113",
    "name": "Double Egg Chicken Fried Rice",
    "category": "Non-Veg Rice Items",
    "price": 160,
    "isVeg": false,
    "tag": "Loaded Protein",
    "isAvailable": true
  },
  {
    "id": "TT-114",
    "name": "Prawns Fried Rice",
    "category": "Non-Veg Rice Items",
    "price": 180,
    "isVeg": false,
    "tag": "Seafood",
    "isAvailable": true
  },
  {
    "id": "TT-115",
    "name": "Schezwan Chicken Fried Rice",
    "category": "Non-Veg Rice Items",
    "price": 160,
    "isVeg": false,
    "tag": "Spicy Schezwan",
    "isAvailable": true
  },
  {
    "id": "TT-116",
    "name": "Special Chicken Fried Rice",
    "category": "Non-Veg Rice Items",
    "price": 200,
    "isVeg": false,
    "tag": "Talking Tables Sp.",
    "isAvailable": true
  },
  {
    "id": "TT-117",
    "name": "Chicken Dum Biryani (5 Pc) + Lollipop Curry (5 Pc)",
    "category": "Bucket Biryani",
    "price": 800,
    "isVeg": false,
    "tag": "Combo Feast (3-4 Pax)",
    "isAvailable": true
  },
  {
    "id": "TT-118",
    "name": "Chicken Dum Bucket + Chilli Chicken Starter",
    "category": "Bucket Biryani",
    "price": 900,
    "isVeg": false,
    "tag": "Mega Feast (4-5 Pax)",
    "isAvailable": true
  },
  {
    "id": "TT-119",
    "name": "Veg Bucket Biryani + Chilli Mushroom + Paneer/Kaju",
    "category": "Bucket Biryani",
    "price": 750,
    "isVeg": true,
    "tag": "Veg Family Bucket",
    "isAvailable": true
  },
  {
    "id": "TT-120",
    "name": "Chicken Dum Thali (Dum Pcs 4 + Boneless Curry + Egg)",
    "category": "Talking Tables Thali's",
    "price": 600,
    "isVeg": false,
    "tag": "Thali Meal",
    "isAvailable": true
  },
  {
    "id": "TT-121",
    "name": "Chicken Wings Thali (Wings 4 Pcs + Curry + Egg + Rumali)",
    "category": "Talking Tables Thali's",
    "price": 700,
    "isVeg": false,
    "tag": "Wings Feast",
    "isAvailable": true
  },
  {
    "id": "TT-122",
    "name": "Chicken Lollipop Thali (Lollipop 5 Pcs + Curry + Egg + Rumali)",
    "category": "Talking Tables Thali's",
    "price": 650,
    "isVeg": false,
    "tag": "Lollipop Special",
    "isAvailable": true
  },
  {
    "id": "TT-123",
    "name": "Chicken Tandoori Thali (Tandoori 1/2 + Tikka Masala + Egg + Naan)",
    "category": "Talking Tables Thali's",
    "price": 800,
    "isVeg": false,
    "tag": "Tandoor Platter",
    "isAvailable": true
  },
  {
    "id": "TT-124",
    "name": "Prawns Thali (Prawn Fry + Prawn Curry + Egg + Butter Naan)",
    "category": "Talking Tables Thali's",
    "price": 900,
    "isVeg": false,
    "tag": "Royal Seafood",
    "isAvailable": true
  },
  {
    "id": "TT-125",
    "name": "Chicken Dum Mandi (Half - 3 Pcs)",
    "category": "Mandi's",
    "price": 400,
    "isVeg": false,
    "tag": "Half (2 Pax)",
    "isAvailable": true
  },
  {
    "id": "TT-126",
    "name": "Chicken Dum Mandi (Full - 5 Pcs)",
    "category": "Mandi's",
    "price": 650,
    "isVeg": false,
    "tag": "Full (4 Pax)",
    "isAvailable": true
  },
  {
    "id": "TT-127",
    "name": "Chicken Wings Mandi (Half - 3 Pcs)",
    "category": "Mandi's",
    "price": 500,
    "isVeg": false,
    "tag": "Half (2 Pax)",
    "isAvailable": true
  },
  {
    "id": "TT-128",
    "name": "Chicken Wings Mandi (Full - 5 Pcs)",
    "category": "Mandi's",
    "price": 750,
    "isVeg": false,
    "tag": "Full (4 Pax)",
    "isAvailable": true
  },
  {
    "id": "TT-129",
    "name": "Tandoori Mandi (Half - 3 Pcs)",
    "category": "Mandi's",
    "price": 500,
    "isVeg": false,
    "tag": "Half (2 Pax)",
    "isAvailable": true
  },
  {
    "id": "TT-130",
    "name": "Tandoori Mandi (Full - 5 Pcs)",
    "category": "Mandi's",
    "price": 750,
    "isVeg": false,
    "tag": "Full (4 Pax)",
    "isAvailable": true
  },
  {
    "id": "TT-131",
    "name": "Chicken Special Mandi All Mixed (Half - 4 Pcs)",
    "category": "Mandi's",
    "price": 600,
    "isVeg": false,
    "tag": "Half Deluxe",
    "isAvailable": true
  },
  {
    "id": "TT-132",
    "name": "Chicken Special Mandi All Mixed (Full - 6 Pcs)",
    "category": "Mandi's",
    "price": 800,
    "isVeg": false,
    "tag": "Full Grand Royal",
    "isAvailable": true
  },
  {
    "id": "TT-133",
    "name": "Prawns Mandi (Half)",
    "category": "Mandi's",
    "price": 800,
    "isVeg": false,
    "tag": "Half Seafood",
    "isAvailable": true
  },
  {
    "id": "TT-134",
    "name": "Prawns Mandi (Full)",
    "category": "Mandi's",
    "price": 1000,
    "isVeg": false,
    "tag": "Full Grand Seafood",
    "isAvailable": true
  }
];

const SEATING_STATIONS = [
  {
    "id": "H-T1",
    "name": "Hall Table T-1",
    "section": "Main Hall",
    "type": "Table",
    "capacity": "4 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "H-T2",
    "name": "Hall Table T-2",
    "section": "Main Hall",
    "type": "Table",
    "capacity": "4 Guests",
    "status": "dining",
    "orderId": "TT-1004",
    "orderTotal": 960,
    "orderTime": "12:15 PM",
    "items": [
      {
        "id": "TT-001",
        "name": "Chilli Paneer",
        "price": 230,
        "qty": 1,
        "total": 230
      },
      {
        "id": "TT-036",
        "name": "Butter Naan",
        "price": 40,
        "qty": 4,
        "total": 160
      },
      {
        "id": "TT-041",
        "name": "Paneer Butter Masala",
        "price": 250,
        "qty": 1,
        "total": 250
      },
      {
        "id": "TT-065",
        "name": "Veg Dum Biryani",
        "price": 320,
        "qty": 1,
        "total": 320
      }
    ]
  },
  {
    "id": "H-T3",
    "name": "Hall Table T-3",
    "section": "Main Hall",
    "type": "Table",
    "capacity": "4 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "H-T4",
    "name": "Hall Table T-4",
    "section": "Main Hall",
    "type": "Table",
    "capacity": "4 Guests",
    "status": "billed",
    "orderId": "TT-1003",
    "orderTotal": 1480,
    "orderTime": "11:45 AM",
    "items": []
  },
  {
    "id": "H-M1",
    "name": "Hall Mandi Cabin M-1",
    "section": "Main Hall",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "dining",
    "orderId": "TT-1002",
    "orderTotal": 1850,
    "orderTime": "12:05 PM",
    "items": [
      {
        "id": "TT-127",
        "name": "Chicken Dum Mandi (Full - 5 Pcs)",
        "price": 650,
        "qty": 2,
        "total": 1300
      },
      {
        "id": "TT-018",
        "name": "Chicken 65",
        "price": 250,
        "qty": 1,
        "total": 250
      },
      {
        "id": "TT-011",
        "name": "Tandoori Chicken (1/2)",
        "price": 250,
        "qty": 1,
        "total": 250
      },
      {
        "id": "TT-036",
        "name": "Butter Naan",
        "price": 40,
        "qty": 1,
        "total": 40
      },
      {
        "id": "TT-034",
        "name": "Tandoori Roti",
        "price": 10,
        "qty": 1,
        "total": 10
      }
    ]
  },
  {
    "id": "H-M2",
    "name": "Hall Mandi Cabin M-2",
    "section": "Main Hall",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "H-M3",
    "name": "Hall Mandi Cabin M-3",
    "section": "Main Hall",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "reserved",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": "07:30 PM",
    "items": []
  },
  {
    "id": "H-M4",
    "name": "Hall Mandi Cabin M-4",
    "section": "Main Hall",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "H-M5",
    "name": "Hall Mandi Cabin M-5",
    "section": "Main Hall",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "dining",
    "orderId": "TT-1005",
    "orderTotal": 2450,
    "orderTime": "12:20 PM",
    "items": [
      {
        "id": "TT-129",
        "name": "Chicken Special Mandi All Mixed (Full - 6 Pcs)",
        "price": 800,
        "qty": 2,
        "total": 1600
      },
      {
        "id": "TT-020",
        "name": "Chicken Manchuria",
        "price": 250,
        "qty": 1,
        "total": 250
      },
      {
        "id": "TT-022",
        "name": "Lollipop Starter (5 pcs)",
        "price": 250,
        "qty": 1,
        "total": 250
      },
      {
        "id": "TT-080",
        "name": "Chicken Fried Rice",
        "price": 200,
        "qty": 1,
        "total": 200
      },
      {
        "id": "TT-036",
        "name": "Butter Naan",
        "price": 40,
        "qty": 3,
        "total": 120
      },
      {
        "id": "TT-034",
        "name": "Tandoori Roti",
        "price": 30,
        "qty": 1,
        "total": 30
      }
    ]
  },
  {
    "id": "H-M6",
    "name": "Hall Mandi Cabin M-6",
    "section": "Main Hall",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C1-M1",
    "name": "Container 1 Cabin C1-M1",
    "section": "Container 1",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "reserved",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": "01:00 PM",
    "items": []
  },
  {
    "id": "C1-M2",
    "name": "Container 1 Cabin C1-M2",
    "section": "Container 1",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "dining",
    "orderId": "TT-1001",
    "orderTotal": 1750,
    "orderTime": "12:10 PM",
    "items": [
      {
        "id": "TT-128",
        "name": "Chicken Special Mandi All Mixed (Half - 3 Pcs)",
        "price": 450,
        "qty": 1,
        "total": 450
      },
      {
        "id": "TT-131",
        "name": "Mutton Juicy Mandi (Full - 5 Pcs)",
        "price": 850,
        "qty": 1,
        "total": 850
      },
      {
        "id": "TT-011",
        "name": "Tandoori Chicken (1/2)",
        "price": 250,
        "qty": 1,
        "total": 250
      },
      {
        "id": "TT-080",
        "name": "Chicken Fried Rice",
        "price": 200,
        "qty": 1,
        "total": 200
      }
    ]
  },
  {
    "id": "C1-M3",
    "name": "Container 1 Cabin C1-M3",
    "section": "Container 1",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C1-M4",
    "name": "Container 1 Cabin C1-M4",
    "section": "Container 1",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C1-M5",
    "name": "Container 1 Cabin C1-M5",
    "section": "Container 1",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C1-M6",
    "name": "Container 1 Cabin C1-M6",
    "section": "Container 1",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C2-M1",
    "name": "Container 2 Cabin C2-M1",
    "section": "Container 2",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C2-M2",
    "name": "Container 2 Cabin C2-M2",
    "section": "Container 2",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "dining",
    "orderId": "TT-1006",
    "orderTotal": 2100,
    "orderTime": "12:28 PM",
    "items": [
      {
        "id": "TT-131",
        "name": "Mutton Juicy Mandi (Full - 5 Pcs)",
        "price": 850,
        "qty": 2,
        "total": 1700
      },
      {
        "id": "TT-080",
        "name": "Chicken Fried Rice",
        "price": 200,
        "qty": 2,
        "total": 400
      }
    ]
  },
  {
    "id": "C2-M3",
    "name": "Container 2 Cabin C2-M3",
    "section": "Container 2",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C2-M4",
    "name": "Container 2 Cabin C2-M4",
    "section": "Container 2",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C2-M5",
    "name": "Container 2 Cabin C2-M5",
    "section": "Container 2",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  },
  {
    "id": "C2-M6",
    "name": "Container 2 Cabin C2-M6",
    "section": "Container 2",
    "type": "Mandi Cabin",
    "capacity": "6-8 Guests",
    "status": "vacant",
    "orderId": null,
    "orderTotal": 0,
    "orderTime": null,
    "items": []
  }
];

if (typeof module !== 'undefined') {
  module.exports = { MENU_ITEMS, SEATING_STATIONS };
}
