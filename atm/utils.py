from fpdf import FPDF


def create_check(date, price, balance, card_number, type):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_xy(10.0, 80.0)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    if type == "balance":
        text = f"""
        Check for operation:
        ...............................
            
        date of operation: {str(date)} \n\r
        balance: {balance} \n\r
        card number: {card_number} \n\r
        operation type: {type} \n\r
        
        """
    else:
        text = f"""
                Check for operation:
                ...............................

                date of operation: {str(date)} \n\r
                price: {price} \n\r
                balance: {balance} \n\r
                card number: {card_number} \n\r
                operation type: {type} \n\r

                """

    pdf.multi_cell(0, 10, txt=text, border=0)
    pdf.output(f'check_{type}.pdf', 'F')
    pass