from maltego_trx.decorator_registry import TransformRegistry

registry = TransformRegistry(
    owner="OSINT Training",
    author="Ali",
    host_url="http://localhost",
    seed_ids=["osint-training"]
)

@registry.register_transform(
    display_name="Twitter Alias to Profile URL",
    input_entity="maltego.Phrase",
    description="Converts Twitter/X alias to profile URL with OSINT metadata",
    output_entities=["maltego.URL"]
)
def twitter_alias_to_url(request, response):
    from transforms.twitter_transform import validate_twitter_alias

    alias = request.Value
    is_valid, cleaned_alias, error_msg = validate_twitter_alias(alias)

    if not is_valid and not cleaned_alias:
        response.addUIMessage(error_msg, messageType="PartialError")
        return response

    # Si l'alias est invalide mais nettoyable, on informe l'utilisateur
    if not is_valid:
        response.addUIMessage(
            f"Alias invalide: {error_msg}",
            messageType="PartialError"
        )

    twitter_url = f"https://x.com/{cleaned_alias}"
    entity = response.addEntity("maltego.URL", twitter_url)

    # Propriétés enrichies
    entity.addProperty("url", "URL", "strict", twitter_url)
    entity.addProperty("short-title", "Title", "loose", f"Profil X de @{cleaned_alias}")
    entity.addProperty("twitter.alias", "Twitter Alias", "strict", cleaned_alias)
    entity.addProperty("twitter.handle", "Twitter Handle", "strict", f"@{cleaned_alias}")

    # Configuration visuelle
    entity.setLinkLabel(f"@{cleaned_alias}")
    entity.setLinkColor("0x0000FF")

    # Notes OSINT
    entity.setNote(
        f"Profil Twitter/X: @{cleaned_alias}\n"
        f"URL: {twitter_url}\n\n"
        f"URLs OSINT additionnelles:\n"
        f"- Recherche tweets: https://x.com/search?q=from:{cleaned_alias}\n"
        f"- Avec réponses: https://x.com/search?q=from:{cleaned_alias}+filter:replies\n"
        f"- Média: https://x.com/{cleaned_alias}/media\n"
        f"- Likes: https://x.com/{cleaned_alias}/likes"
    )

    return response