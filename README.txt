CIVIL ENGINEERING EXAM SIMULATOR
================================

Requirements:
- Python 3.6+
- Pillow (for images): pip install Pillow

How to Run:
1. Create a folder named "ce_exam_simulator"
2. Save exam_simulator.py and question_bank.json in it
3. Create a subfolder "figures" and save the two PNGs inside
4. Open terminal in "ce_exam_simulator" folder
5. Run: pip install Pillow
6. Run: python exam_simulator.py

Features:
- Randomized exam with figure support
- Situational groups preserved
- Visual answer key with ✅/❌
- Section timers and breaks

To add more figures:
1. Save PNG in figures/
2. Add "figure": "figures/your_image.png" to a question in question_bank.json