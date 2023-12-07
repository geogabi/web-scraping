import matplotlib
import matplotlib.pyplot as plt
import io
from flask import make_response


# Create statistics for every product base by first price
def product_statistic(new_number, previous_number):
    if new_number > previous_number:
        x = abs(new_number - previous_number)
        percent = round((x / previous_number) * 100)
        return f'+{percent}%'
    elif new_number < previous_number:
        x = abs(previous_number - new_number)
        percent = round((x / previous_number) * 100)
        return f'-{percent}%'
    else:
        x = abs(new_number - previous_number)
        percent = round((x / previous_number) * 100)
        return f'+{percent}%'


# Create statistics for every item base by every price
def items_statistics(new_number, previous_number):
    if new_number > previous_number:
        x = abs(new_number - previous_number)
        percent = round((x / previous_number) * 100)
        return f'+{percent}%'
    elif new_number < previous_number:
        x = abs(previous_number - new_number)
        percent = round((x / previous_number) * 100)
        return f'-{percent}%'
    else:
        x = abs(new_number - previous_number)
        percent = round((x / previous_number) * 100)
        return f'+{percent}%'


# Create plot using matplotlib
def create_graphic(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.title('Price tracker')
    plt.xlabel('Data')
    plt.ylabel('Price')

    buffer = io.BytesIO()
    fig.set_size_inches(11, 7)
    fig.savefig(buffer, format='png', dpi=70)
    buffer.seek(0)

    _response = make_response(buffer.getvalue())
    _response.mimetype = 'image/png'
    matplotlib.pyplot.close(fig)

    return _response
