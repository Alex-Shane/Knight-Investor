

window.onload = function() {
    var period = document.getElementById("period")
    var exchange = document.getElementById("exchange")
    var industry = document.getElementById("industry")
}

function setIndustryOptions() {
    var exchangeObject = {
        "SP500": ['assets', 'tech'],
        "NASDAQ": ['just', 'tech'],
        "DOW": ['small'],
        "NYSE": ['has', 'everything']
      }
    //empty Chapters dropdown
    industry.length = 1;
    //display correct values
    exchangeVal = exchange.value
    for (var i = 0; i < exchangeObject[exchangeVal].length; i++) {
      industry.options[industry.options.length] = new Option(exchangeObject[exchangeVal][i], exchangeObject[exchangeVal][i]);
    }
  }
