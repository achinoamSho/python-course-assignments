# Cell Culture Calculator

I wanted to calculate how much cell suspension to transfer from one culture plate to another based on the desired confluency and plate sizes. I often work in the tissue culture room, so I made this tool to make my lab mates’ (and my own) life easier.

## Features
- 3 input methods:
  - Command-line (CLI)
  - Interactive (input)
  - GUI (Tkinter), also Validates user input, and includes preset plate sizes

## Calculation
$\text{Volume to take} = V_\text{current} \cdot \frac{C_\text{desired} \cdot A_\text{destination}}{C_\text{current} \cdot A_\text{current}}$

**Where:**
- **C** = Confluency (%)
- **A** = Area (cm²)
- **V** = Volume (mL)

## AI 
I used ChatGPT (GPT-5) to assist with:
- Writing the GUI using `tkinter`
- Debugging error handling

### Prompts used
> "I want to use GUI for calculating the volume I need to take from a plate with cultured cells by certain confluency I'm aiming for.."

> "Could you improve the GUI to make it easier to use, with dropdown menus for plate sizes?"

> "I don’t want any pre-filled values when the program opens, can we make the fields empty instead?" 

