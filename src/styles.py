# styles.py

my_style = """
QLineEdit {
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 6px 10px;
    background-color: #008a91;
    color: #333;
    font-size: 14px;
}

QLineEdit:focus {
    border: 1px solid #0078d7;
    background-color: #ffffff;
}

QLineEdit::placeholder {
    color: #ffffff;
}

QPushButton { 
    padding: 5px 10px; 
    border-radius: 5px; 
    background-color: #4CAF50; 
    color: white; 
} 

  QLabel {
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 600;
        padding: 2px 4px;
        letter-spacing: 0.5px;
    }
"""

btn_sheet = """
QPushButton {
    color: rgb(255, 255, 255);
    background-color: #272757;   
    border: 0px solid;
    text-align: center;  
    border-radius: 10px;
}

QPushButton:hover {
    background-color: #9575cd;
    font-size: 17px; 
    border-radius: 10px;
    margin: 5px;
}
"""

combo_sheet = '''
 QComboBox {
        background-color: #2c2f4c;
        color: white;
        border: 1px solid #5a5f7a;
        padding: 6px 10px;
        font-size: 14px;
        border-radius: 6px;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #5a5f7a;
    }

    QComboBox::down-arrow {
        image: url(:/icons/down_arrow.png); /* Replace with your own icon path */
        width: 12px;
        height: 12px;
    }

    QComboBox QAbstractItemView {
        background-color: #1e1f3d;
        color: white;
        selection-background-color: #3a3d6d;
        border: 1px solid #5a5f7a;
        font-size: 14px;
    }'''
