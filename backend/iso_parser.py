import pandas as pd
from lxml import etree
from datetime import datetime

class ISO20022Parser:
    """
    High-performance XML parser for ISO 20022 camt.053 bank statements.
    Extracts structured remittance data for the SmartMatching Engine.
    """
    
    def __init__(self):
        # XML Namespaces standard for ISO 20022
        self.ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02'}

    def parse_camt053(self, xml_content):
        """
        Parses raw XML and returns a flattened Pandas DataFrame.
        """
        try:
            tree = etree.fromstring(xml_content)
            transactions = []

            # Navigate to the Entry level (Ntry) in the ISO schema
            entries = tree.xpath('//ns:Ntry', namespaces=self.ns)

            for entry in entries:
                # Extracting Core ISO 20022 Fields
                amt = entry.xpath('.//ns:Amt/text()', namespaces=self.ns)[0]
                ccy = entry.xpath('.//ns:Amt/@Ccy', namespaces=self.ns)[0]
                status = entry.xpath('.//ns:Sts/text()', namespaces=self.ns)[0]
                booking_date = entry.xpath('.//ns:BookgDt/ns:Dt/text()', namespaces=self.ns)[0]
                
                # Transaction Details (Payer & Reference)
                payer = entry.xpath('.//ns:RltdPties/ns:Dbtr/ns:Nm/text()', namespaces=self.ns)
                remittance = entry.xpath('.//ns:RmtInf/ns:Ustrd/text()', namespaces=self.ns)
                
                transactions.append({
                    "Bank_Ref": f"ISO-{datetime.now().strftime('%y%m')}-{len(transactions)}",
                    "Amount": float(amt),
                    "Currency": ccy,
                    "Payer_Name": payer[0] if payer else "Unknown Payer",
                    "Reference_Text": remittance[0] if remittance else "No Ref Provided",
                    "Date": booking_date,
                    "Status": "Unmatched"
                })

            return pd.DataFrame(transactions)
        
        except Exception as e:
            print(f"ISO Parsing Error: {e}")
            return pd.DataFrame()

    def generate_iso_sample(self):
        """Creates a mock ISO 20022 XML string for testing S11 logic."""
        return """
        <Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.02">
            <BkToCstmrStmt>
                <Stmt>
                    <Ntry>
                        <Amt Ccy="EUR">45000.00</Amt>
                        <Sts>BOOK</Sts>
                        <BookgDt><Dt>2026-02-01</Dt></BookgDt>
                        <RltdPties>
                            <Dbtr><Nm>Tesla Motors Gmbh</Nm></Dbtr>
                        </RltdPties>
                        <RmtInf><Ustrd>INV-2026001 settlement</Ustrd></RmtInf>
                    </Ntry>
                </Stmt>
            </BkToCstmrStmt>
        </Document>
        """
