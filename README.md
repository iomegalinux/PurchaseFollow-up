### Utilisation de l'Application

1. **Paramètres de l'Email :**

   - Naviguez vers l'onglet **Paramètres de l'Email**.

   - **Serveur SMTP :** Entrez l'adresse de votre serveur SMTP (par exemple, `smtp.gmail.com` pour Gmail).

   - **Port SMTP :** Entrez le numéro de port (généralement `587` pour TLS).

   - **Nom d'Utilisateur SMTP :** Votre adresse email utilisée pour envoyer les emails.

   - **Mot de Passe SMTP :** Le mot de passe de votre compte email.

   - **Nom de Votre Entreprise :** Le nom de votre entreprise à inclure dans la signature de l'email.

2. **Suivi des Commandes en Retard :**

   - Naviguez vers l'onglet **Suivi des Commandes en Retard**.

   - **Télécharger CSV :** Cliquez sur le bouton de téléchargement et sélectionnez votre fichier CSV de commandes en retard.

   - **Voir les Données :** Après le téléchargement, les données seront affichées dans une grille interactive.

   - **Sélectionner les Commandes :** Utilisez les cases à cocher pour sélectionner les commandes que vous souhaitez suivre.

   - **Envoyer les Emails de Suivi :** Cliquez sur le bouton **Suivi** pour envoyer des emails aux fournisseurs sélectionnés.

### Structure du Fichier CSV

L'application attend que le fichier CSV téléchargé contienne les colonnes suivantes :

- **vendor_no :** Un identifiant unique pour le fournisseur (par exemple, `V12345`).

- **email :** L'adresse email du fournisseur (par exemple, `fournisseur@example.com`).

- **product :** Le nom du produit en rupture de stock (par exemple, `Widget A`).

- **quantity :** La quantité du produit en rupture de stock (par exemple, `100`).

- **due_date :** La date prévue de livraison au format `YYYY-MM-DD` (par exemple, `2024-01-15`).

**Exemple de CSV :**

| vendor_no | email                   | product  | quantity | due_date   |
|-----------|-------------------------|----------|----------|------------|
| V12345    | fournisseur1@example.com | Widget A | 100      | 2024-01-10 |
| V67890    | fournisseur2@example.com | Widget B | 50       | 2024-01-15 |

### Détails des Paramètres de l'Email

Pour configurer correctement les paramètres de l'email, assurez-vous de ce qui suit :

- **Serveur SMTP :** C'est l'adresse du serveur SMTP de votre fournisseur d'email. Les serveurs SMTP courants incluent :

  - Gmail : `smtp.gmail.com`

  - Outlook : `smtp.office365.com`

  - Yahoo : `smtp.mail.yahoo.com`

- **Port SMTP :**

  - **TLS :** Utilisez le port `587`.

  - **SSL :** Utilisez le port `465`.

- **Nom d'Utilisateur SMTP :** Il s'agit de votre adresse email complète (par exemple, `votre_email@exemple.com`).

- **Mot de Passe SMTP :** Pour des raisons de sécurité, envisagez d'utiliser un [mot de passe d'application](https://support.google.com/accounts/answer/185833) si vous utilisez Gmail ou des services similaires qui offrent des mots de passe spécifiques aux applications.

- **Nom de Votre Entreprise :** Cela apparaîtra dans la signature de l'email pour personnaliser la communication.

**Important :** Assurez-vous que votre compte email autorise l'accès SMTP. Vous devrez peut-être ajuster les paramètres de sécurité ou activer l'accès pour les applications moins sécurisées en fonction de votre fournisseur d'email.

## Meilleures Pratiques

- **Variables d'Environnement :** Pour une sécurité renforcée, stockez les informations sensibles comme les identifiants SMTP dans des variables d'environnement au lieu de les coder en dur dans le code.

- **Environnements Virtuels :** Utilisez toujours un environnement virtuel pour gérer les dépendances de votre projet et éviter les conflits.

- **Gestion des Dépendances :** Mettez régulièrement à jour vos dépendances et utilisez des outils comme `pip freeze` pour maintenir un fichier `requirements.txt`.

## Dépannage

- **Problèmes de Téléchargement CSV :**

  - Assurez-vous que votre fichier CSV contient toutes les colonnes requises : `vendor_no`, `email`, `product`, `quantity`, `due_date`.

  - Vérifiez que la `due_date` est au format correct `YYYY-MM-DD`.

- **Échecs lors de l'Envoi des Emails :**

  - Vérifiez l'exactitude de vos paramètres SMTP.

  - Assurez-vous que votre réseau autorise les connexions SMTP sortantes.

  - Vérifiez que votre compte email dispose des autorisations nécessaires pour envoyer des emails via SMTP.

- **Erreurs de l'Application :**

  - Consultez le terminal pour tout message d'erreur lors de l'exécution de l'application Streamlit.

  - Utilisez `flake8` pour analyser votre code et identifier les problèmes de syntaxe :

    ```
    flake8 backorder_followup.py
    ```

## Contribution

Les contributions sont les bienvenues ! Veuillez forker le dépôt et soumettre une pull request avec vos améliorations.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

### Using the Application

1. **Email Settings:**

   - Navigate to the **Email Settings** tab.

   - **SMTP Server:** Enter your SMTP server address (e.g., `smtp.gmail.com` for Gmail).

   - **SMTP Port:** Enter the port number (commonly `587` for TLS).

   - **SMTP Username:** Your email address used to send emails.

   - **SMTP Password:** The password for your email account.

   - **Your Company Name:** The name of your company to be included in the email signature.

2. **Back Order Follow-up:**

   - Navigate to the **Back Order Follow-up** tab.

   - **Upload CSV:** Click the upload button and select your back order CSV file.

   - **View Data:** After uploading, the data will be displayed in an interactive grid.

   - **Select Orders:** Use the checkboxes to select the orders you want to follow up on.

   - **Send Follow-up Emails:** Click the **Follow-up** button to send emails to the selected vendors.

### CSV File Structure

The application expects the uploaded CSV file to have the following columns:

- **vendor_no:** A unique identifier for the vendor (e.g., `V12345`).

- **email:** The vendor's email address (e.g., `vendor@example.com`).

- **product:** The name of the back-ordered product (e.g., `Widget A`).

- **quantity:** The quantity of the product back-ordered (e.g., `100`).

- **due_date:** The expected fulfillment date in `YYYY-MM-DD` format (e.g., `2024-01-15`).

**Example CSV:**

| vendor_no | email               | product  | quantity | due_date   |
|-----------|---------------------|----------|----------|------------|
| V12345    | vendor1@example.com | Widget A | 100      | 2024-01-10 |
| V67890    | vendor2@example.com | Widget B | 50       | 2024-01-15 |

### Email Settings Details

To configure the email settings correctly, ensure the following:

- **SMTP Server:** This is the address of your email provider's SMTP server. Common SMTP servers include:

  - Gmail: `smtp.gmail.com`

  - Outlook: `smtp.office365.com`

  - Yahoo: `smtp.mail.yahoo.com`

- **SMTP Port:**

  - **TLS:** Use port `587`.

  - **SSL:** Use port `465`.

- **SMTP Username:** This should be your full email address (e.g., `your_email@example.com`).

- **SMTP Password:** For security reasons, consider using an [App Password](https://support.google.com/accounts/answer/185833) if you're using Gmail or similar services that offer app-specific passwords.

- **Your Company Name:** This will appear in the email signature to personalize the communication.

**Important:** Ensure that your email account allows SMTP access. You may need to adjust security settings or enable access for less secure apps depending on your email provider.

## Best Practices

- **Environment Variables:** For enhanced security, store sensitive information like SMTP credentials in environment variables instead of hardcoding them.

- **Virtual Environments:** Always use a virtual environment to manage your project's dependencies and avoid conflicts.

- **Dependency Management:** Regularly update your dependencies and use tools like `pip freeze` to maintain a `requirements.txt` file.

## Troubleshooting

- **CSV Upload Issues:**

  - Ensure your CSV file has all the required columns: `vendor_no`, `email`, `product`, `quantity`, `due_date`.

  - Verify that the `due_date` is in the correct `YYYY-MM-DD` format.

- **Email Sending Failures:**

  - Double-check your SMTP settings for accuracy.

  - Ensure that your network allows outbound SMTP connections.

  - Verify that your email account has the necessary permissions to send emails via SMTP.

- **Application Errors:**

  - Check the terminal for any error messages when running the Streamlit app.

  - Use `flake8` to lint your code and identify any syntax issues:

    ```
    flake8 backorder_followup.py
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
