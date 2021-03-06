from speakerKey import KEY


class Speak:
    def __init__(self, text, file_format='mp3', quality='hi', lang='ru-RU', speaker='alyss', speed=1.0,
                 emotion='neutral', key=KEY):
        """
        :param text:
        Текст, который нужно озвучить. Для передачи слов-омографов используйте + перед ударной гласной.
        (Например, гот+ов или def+ect.) Ограничение на длину строки: 2000 байт.

        :param file_format:
        Расширение синтезируемого файла (его формат). Допустимые значения:
            ● mp3 — аудио в формате MPEG, медиаконтейнер MPEG-1 Audio Layer 3;
            ● wav — аудио в формате PCM 16 бит, медиаконтейнер WAV;
            ● opus — аудио в формате Opus, в качестве контейнера используется OGG.

        :param quality:(необязательный)
        Частота дискретизации и битрейт синтезируемого PCM-аудио (медиаконтейнер WAV). Допустимые значения:
            ● hi — частота дискретизации 48 кГц и битрейт 768 кб/c;
            ● lo — частота дискретизации 8 кГц и битрейт 128 кб/c.
        По умолчанию quality=hi.

        Обратите внимание, параметр quality влияет на характеристики аудио только если file_format=wav.

        :param lang:
        Допустимые значения: ru-RU — русский язык, en-US — английский язык, uk-UK — украинский язык, tr-TR — турецкий язык.
        Язык не определяется автоматически. Значение параметра по умолчанию: ru‑RU.

        :param speaker:
        Голос синтезированной речи. Можно выбрать один из следующих голосов:
            женские голоса: jane, oksana, alyss и omazh;
            мужские голоса: zahar и ermil.

        :param speed: (необязательный)
        Скорость (темп) синтезированной речи. Скорость речи задается дробным числом в диапазоне от 0.1 до 3.0. Где:
            ● 3.0 — самый быстрый темп;
            ● 1.0 — средняя скорость человеческой речи;
            ● 0.1 — самый медленный темп.

        :param emotion: (необязательный)
        Эмоциональная окраска голоса. Допустимые значения:
            ● good — радостный, доброжелательный;
            ● evil — раздраженный;
            ● neutral — нейтральный (используется по умолчанию).

        P.S.: Значение neutral ранее называлась mixed (смешанная окраска голоса).
        Сейчас mixed поддерживается, но считается устаревшим.

        :param key: API‑ключ.
        Вы можете бесплатно (https://tech.yandex.ru/speechkit/cloud/doc/guide/concepts/faq-docpage/#free) получить
         API‑ключ в Кабинете разработчика. (https://developer.tech.yandex.ru/)

        :return: Путь до файла
        """
        import os
        from urllib.parse import urlencode

        file_format = 'opus' if file_format == 'ogg' else file_format

        def check_text():
            class TextError(Exception):
                pass

            try:
                if type(text) is str:
                    open('.speaker_text.nomedia', 'w').write(text)
                    if sum(1 for _ in open('.speaker_text.nomedia', 'rb').read()) > 2000:
                        raise TextError
                else:
                    raise TextError
                return True
            finally:
                os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.speaker_text.nomedia'))

        def check_format():
            class FormatError(Exception):
                pass

            formats = ['mp3', 'wav', 'opus']
            if file_format not in formats:
                raise FormatError
            return ['.mp3', '.wav', '.ogg'][formats.index(file_format)]

        def check_quality():
            class QualityError(Exception):
                pass

            if quality not in ['lo', 'hi']:
                raise QualityError
            return True

        def check_lang():
            class LangError(Exception):
                pass

            if lang not in ['ru-RU', 'en-US', 'uk-UK', 'tr-TR']:
                raise LangError
            return True

        def check_speaker():
            class SpeakerError(Exception):
                pass

            if speaker not in ['jane', 'oksana', 'alyss', 'omazh', 'zahar', 'ermil']:
                raise SpeakerError
            return True

        def check_speed():
            class SpeedError(Exception):
                pass

            if type(speed) is int or type(speed) is float:
                if not (0.1 <= speed <= 3):
                    raise SpeedError
            else:
                raise SpeedError
            return True

        def check_emotion():
            class EmotionError(Exception):
                pass

            if emotion not in ['evil', 'neutral', 'good', 'mixed']:
                raise EmotionError
            return True

        if all([check_text(), check_speed(), check_speaker(), check_speaker(), check_lang(), check_emotion(),
                check_format(), check_quality()]):
            file_name = ''.join(map(lambda x: ('_' if x.isspace() else '') if not x.isalnum() else x, text))[:35]
            file_name += '(' + speaker + ')' + check_format()
            params = {'text': text, 'format': file_format, 'quality': quality, 'lang': lang, 'speaker': speaker,
                      'speed': speed, 'emotion': emotion, 'key': key}
            url = 'https://tts.voicetech.yandex.net/generate?' + urlencode(params)
            self.file_name, self.url = file_name, url

    def __bytes__(self):
        from urllib.request import urlopen
        return bytes([i for i in urlopen(self.url).read()])

    def save(self, dir='', file_name=None):
        import os
        file_name = self.file_name if file_name is None else file_name+self.file_name[-4:]
        with open(os.path.join(dir, file_name), 'wb') as file:
            file.write(bytes(self))
        return (dir, file_name) if dir else (os.getcwd(), file_name)
