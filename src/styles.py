# styles.py

my_style = """
QLineEdit {
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 6px 10px;
    background-color: #B3B3B3;
    color: #333;
    font-size: 14px;
}

QLineEdit:focus {
    border: 1px solid #0078d7;
    background-color: #ffffff;
}

QLineEdit::placeholder {
    color: white;
}

QPushButton { 
    padding: 5px 10px; 
    border-radius: 5px; 
    background-color: #4CAF50; 
    color: white; 
} 

QLabel {
    color: white;
    font-family: 'Source Code Pro' ;
}
QLabel#headers {
    color: white;
    font-family: 'Fira Code' ;
    font-size: 17px;
}
"""

btn_sheet = """
QPushButton {
    color: rgb(255, 255, 255);
    background-color: #636B2F;   
    border: 0px solid;
    text-align: center;  
    border-radius: 10px;
}

QPushButton:hover {
    background-color: #D4DE95;
    font-size: 17px; 
    border-radius: 10px;
    margin: 5px;
}
"""
combo_sheet = '''
 QComboBox {
        background-color: #B3B3B3;
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
        border-left: 1px solid #B3B3B3;
    }

    QComboBox QAbstractItemView {
        background-color: #B3B3B3;
        color: white;
        selection-background-color: #3a3d6d;
        border: 1px solid #5a5f7a;
        font-size: 14px;
    }'''
