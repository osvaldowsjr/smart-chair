from datetime import datetime


# Classe que gerencia a temperatura do ambiente
class tempManager:
    def __init__(self, temp: float):
        self.temp = temp

    def getDisplayMsg(self):
        season = self.getSeason()

        if season in ['summer', 'spring']:
            if self.temp >= 26.0:
                # Integração com ALEXA/GOOGLE HOME para configurar temperatura
                return "A temperatura está alta! Abra a janela ou ligue o ar %.2f °C" % self.temp
            elif self.temp <= 23.0:
                # Integração com ALEXA/GOOGLE HOME para configurar temperatura
                return "A temperatura está baixa! Feche a janela ou ligue o aquecedor %.2f °C" % self.temp
            else:
                return str(self.temp)
        else:
            if self.temp >= 23.0:
                # Integração com ALEXA/GOOGLE HOME para configurar temperatura
                return "A temperatura está alta! Abra a janela ou ligue o ar %.2f °C" % self.temp
            elif self.temp <= 20.0:
                # Integração com ALEXA/GOOGLE HOME para configurar temperatura
                return "A temperatura está baixa! Feche a janela ou ligue o aquecedor %.2f °C" % self.temp
            else:
                return str(self.temp)

    @staticmethod
    def getSeason():
        doy = datetime.today().timetuple().tm_yday
        fall = range(80, 172)
        winter = range(172, 264)
        spring = range(264, 355)
        # summer = everything else

        if doy in spring:
            return 'spring'
        elif doy in winter:
            return 'winter'
        elif doy in fall:
            return 'fall'
        else:
            return 'summer'
