from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    try:
        # Get Configuration Settings

        load_dotenv()
        ai_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
        ai_key = os.getenv("AI_SERVICE_KEY")

        # Create client using endpoint and key

        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(
            endpoint=ai_endpoint, credential=credential
        )

        # Analyze each text file in the reviews folder

        reviews_folder = "reviews"
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print("\n-------------\n" + file_name)
            text = open(
                os.path.join(reviews_folder, file_name), encoding="utf8"
            ).read()
            print("\n" + text)

            analysis_text = [text]

            # Get language

            detect_language_result = ai_client.detect_language(
                documents=analysis_text
            )
            # type(detect_language_result): List

            detected_language = detect_language_result[0]
            # type(detected_language): azure.ai.textanalytics._models.DetectLanguageResult

            primary_language = detected_language.primary_language
            # type(primary_language): azure.ai.textanalytics._models.DetectedLanguage

            print("\nLanguage: {}".format(primary_language.name))

            # Get sentiment

            sentiment_analysis = ai_client.analyze_sentiment(
                documents=analysis_text
            )
            # type(sentiment_analysis)): List

            detected_sentiment = sentiment_analysis[0]
            # type(detected_sentiment)): azure.ai.textanalytics._models.AnalyzeSentimentResult

            print("\nSentiment: {}".format(detected_sentiment.sentiment))

            # Get key phrases

            phrase_analysis = ai_client.extract_key_phrases(
                documents=analysis_text
            )
            # type(phrase_analysis)): List

            phrase_extraction_results = phrase_analysis[0]
            # type(phrase_extraction_results)): azure.ai.textanalytics._models.ExtractKeyPhrasesResult

            key_phrases = phrase_extraction_results.key_phrases
            # type(key_phrases): List

            if len(key_phrases) > 0:
                print("\nKey Phrases:")
                for phrase in key_phrases:
                    print("\t{}".format(phrase))

            # Get entities

            entities_analysis = ai_client.recognize_entities(
                documents=analysis_text
            )
            # type(entities_analysis)): List

            entities_extraction_results = entities_analysis[0]
            # type(entities_extraction_results)): azure.ai.textanalytics._models.RecognizeEntitiesResult

            entities = entities_extraction_results.entities
            # type(entities)): List

            if len(entities) > 0:
                print("\nEntities:")
                for entity in entities:
                    ent_text = entity.text
                    ent_cat = entity.category
                    print("\t{} ({})".format(ent_text, ent_cat))
            # type(entity)): azure.ai.textanalytics._models.CategorizedEntity
            # type(ent_text): str
            # type(ent_cat): str

            # Get linked entities

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
