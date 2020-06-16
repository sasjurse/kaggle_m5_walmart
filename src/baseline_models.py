from model_utilities import write_validation_results_to_db


class SingleColumnPredictor:

    def __init__(self, column_name, divisor=None):
        self.column_name = column_name
        if divisor:
            self.divisor = divisor

    def predict(self, train):
        if self.divisor:
            return train[self.column_name] / self.divisor
        else:
            return train


column = 'wa_adjusted_quantity_last_7'
write_validation_results_to_db(model=SingleColumnPredictor(column, divisor=7),
                               model_name=column,
                               params='Single column'
                               )

column = 'quantity_last_7'
write_validation_results_to_db(model=SingleColumnPredictor(column, divisor=7),
                               model_name=column,
                               params='Single column'
                               )

column = 'quantity_last_3'
write_validation_results_to_db(model=SingleColumnPredictor(column, divisor=3),
                               model_name=column,
                               params='Single column'
                               )

