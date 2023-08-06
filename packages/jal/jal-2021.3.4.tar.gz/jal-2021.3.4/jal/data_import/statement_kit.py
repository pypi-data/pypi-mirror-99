import logging
import re
from datetime import datetime, timezone, timedelta
import pandas

from jal.widgets.helpers import g_tr
from jal.db.update import JalDB
from jal.constants import Setup, DividendSubtype


# -----------------------------------------------------------------------------------------------------------------------
class KITFinance:
    Header = "КИТ Финанс (АО)"
    AccountPattern = "(?P<ACCOUNT>.*)-(.*)"
    PeriodPattern = "(?P<S>\d\d\.\d\d\.\d\d\d\d) - (?P<E>\d\d\.\d\d\.\d\d\d\d)"

    def __init__(self, parent, filename):
        self._parent = parent
        self._filename = filename
        self._statement = None
        self._account_id = 0

    def load(self):
        self._statement = pandas.read_excel(self._filename, header=None, na_filter=False)
        if not self.validate():
            return False
        self.load_stock_deals()
        # self.load_cash_tranactions()
        return True

    def validate(self):
        if self._statement[4][0] != self.Header:
            logging.error(g_tr('KIT', "Can't find KIT Finance report header"))
            return False
        parts = re.match(self.AccountPattern, self._statement[5][5], re.IGNORECASE)
        if parts is None:
            logging.error(g_tr('KIT', "Can't parse KIT Finance account number"))
            return False
        account_name = parts.groupdict()['ACCOUNT']
        parts = re.match(self.PeriodPattern, self._statement[5][8], re.IGNORECASE)
        if parts is None:
            logging.error(g_tr('KIT', "Can't parse KIT Finance statement period"))
            return False
        statement_dates = parts.groupdict()
        report_start = int(datetime.strptime(statement_dates['S'], "%d.%m.%Y").replace(tzinfo=timezone.utc).timestamp())
        if not self._parent.checkStatementPeriod(account_name, report_start):
            return False
        logging.info(g_tr('KIT', "Loading KIT Finance statement for account ") +
                     f"{account_name}: {statement_dates['S']} - {statement_dates['E']}")
        self._account_id = self._parent.findAccountID(account_name)
        return True

    def find_section_start(self, header, columns) -> (int, dict):
        start_row = -1
        headers = {}
        for i, row in self._statement.iterrows():
            if row[0] == header:
                start_row = i + 1  # points to columns header row
                break
        if start_row > 0:
            for col in range(self._statement.shape[1]):  # Load section headers from next row
                headers[self._statement[col][start_row]] = col
        column_indices = {column: headers.get(columns[column], -1) for column in columns}
        for idx in column_indices:
            if column_indices[idx] < 0:
                logging.error(g_tr('KIT', "Column not found: ") + idx)
                start_row = -1
        start_row += 1
        return start_row, column_indices

    def load_stock_deals(self):
        cnt = 0
        columns = {
            "number": "Номер\nсделки",
            "date": "Дата сделки",
            "time": "Время сделки",
            "asset": "Наименование\nЦБ",
            "isin": "ISIN",
            "B/S": "Тип операции",
            "price": "Цена сделки ",
            "qty": "Количество",
            "amount": "Сумма сделки",
            "accrued_int": " НКД",
            "settlement": "Дата поставки\n(план.)",
            "fee_ex": "Комиссия\nТС",
            "fee_broker": "Комиссия\nброкера"
        }

        row, headers = self.find_section_start("Заключенные сделки с ценными бумагами", columns)
        if row < 0:
            return False
        while row < self._statement.shape[0]:
            if self._statement[0][row] == '' and self._statement[0][row + 1] == '':
                break
            asset_id = self._parent.findAssetID('', isin=self._statement[headers['isin']][row],
                                                name=self._statement[headers['asset']][row])
            if self._statement[headers['B/S']][row] == 'Покупка':
                amount = -self._statement[headers['amount']][row]
                qty = self._statement[headers['qty']][row]
                bond_interest = -self._statement[headers['accrued_int']][row]
            elif self._statement[headers['B/S']][row] == 'Продажа':
                amount = self._statement[headers['amount']][row]
                qty = -self._statement[headers['qty']][row]
                bond_interest = self._statement[headers['accrued_int']][row]
            else:
                row += 1
                logging.warning(g_tr('KIT', "Unknown trade type: ") + self._statement[headers['B/S']][row])
                continue
            price = self._statement[headers['price']][row]
            fee = round(abs(self._statement[headers['fee_ex']][row] + self._statement[headers['fee_broker']][row]), 8)
            if abs(abs(price * qty) - amount) >= Setup.DISP_TOLERANCE:
                price = abs(amount / qty)
            number = self._statement[headers['number']][row]
            # Dates are loaded as datetime objects but time is loaded as string
            t_date = self._statement[headers['date']][row]
            t_time = datetime.strptime(self._statement[headers['time']][row], "%H:%M:%S").time()
            trade_datetime = t_date + timedelta(hours=t_time.hour, minutes=t_time.minute, seconds=t_time.second)
            timestamp = int(trade_datetime.replace(tzinfo=timezone.utc).timestamp())
            settlement = int(self._statement[headers['settlement']][row].replace(tzinfo=timezone.utc).timestamp())
            JalDB().add_trade(self._account_id, asset_id, timestamp, settlement, number, qty, price, -fee)
            if bond_interest != 0:
                JalDB().add_dividend(DividendSubtype.BondInterest, timestamp, self._account_id, asset_id,
                                     bond_interest, "НКД", number)
            cnt += 1
            row += 1
        logging.info(g_tr('KIT', "Trades loaded: ") + f"{cnt}")
