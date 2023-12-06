Para criar um executável do seu script Python utilizando o PyQt6 e o módulo requests, siga estes passos:

Prepare o Ambiente de Desenvolvimento:
Certifique-se de que você está trabalhando com a versão correta do Python para a qual você deseja construir o executável. Você mencionou que deseja fazer isso como usuário, não como administrador, então você deve ter o Python instalado em um nível de usuário e ter permissão para criar ambientes virtuais e instalar pacotes.

1- Crie um Ambiente Virtual:
Abra um terminal (no Windows, você pode usar o CMD ou PowerShell) e navegue até o diretório do seu projeto:
    cd caminho/para/seu/projeto

2- Crie um ambiente virtual utilizando o módulo venv:
    python -m venv env

3- Ative o ambiente virtual:
No Windows (cmd.exe):
    env\Scripts\activate

No Windows (PowerShell):
    env\Scripts\Activate.ps1

No Unix ou MacOS (bash/shell):
    source env/bin/activate

4- Instale as Dependências:
Com o ambiente virtual ativado, instale o PyQt6 e o módulo requests:
    pip install PyQt6 requests

5- Instale o PyInstaller:
Ainda com o ambiente virtual ativado, instale o PyInstaller:
    pip install pyinstaller

6- Crie o Executável:
Utilize o PyInstaller para criar o executável do seu script:
    pyinstaller --onefile --windowed "nome_do_arquivo"
    pyinstaller --onefile --windowed --icon=img/icone_ELITEACO.ico eliaApp-061223-01.py      (com ícone)

7- Teste o Executável:
Após o PyInstaller terminar, ele criará uma pasta dist no mesmo diretório do seu script. Dentro dessa pasta, você encontrará o arquivo executável. Execute-o para garantir que está funcionando corretamente.

8- Solucione Problemas de Empacotamento:
Se o executável não funcionar corretamente (por exemplo, se faltar algum módulo), você pode precisar ajustar as opções do PyInstaller, como adicionar --hidden-import para módulos que não estão sendo detectados automaticamente.

9- Distribuição:
Se o executável estiver funcionando como esperado, você pode distribuí-lo para outros usuários. Tenha em mente que a compilação do PyInstaller é específica para o sistema operacional em que foi criada, portanto, você precisará criar uma compilação separada para cada sistema operacional que deseja suportar.

Lembre-se de substituir suas chaves de API reais antes de distribuir seu aplicativo. As chaves não devem ser armazenadas em texto simples dentro do código quando o aplicativo é distribuído.

--------------------------------------------------------------------

Quando você faz alterações no seu script Python e deseja gerar um novo executável, geralmente é uma boa prática limpar os artefatos de build anteriores para evitar qualquer confusão ou conflito com arquivos antigos. Aqui está como você pode proceder:

1- Limpe os Artefatos Antigos:

Exclua a pasta dist/, que contém o executável anterior.
Exclua a pasta build/, que contém arquivos de intermediários de build.
Exclua o arquivo .spec que foi gerado pelo PyInstaller. Este arquivo contém configurações de build, e se você quiser que o PyInstaller gere um novo com as configurações padrão, você deve excluí-lo. Se você tiver feito modificações personalizadas no arquivo .spec que deseja manter, não o exclua.
Você pode fazer isso manualmente usando o explorador de arquivos ou usando o terminal com os seguintes comandos (no diretório do projeto):

No Windows (cmd.exe ou PowerShell):
    rmdir /s /q build dist
    del /f /q eliaApp-PyQt6-2023_12_01.spec

No Unix ou MacOS (bash/shell):
    rm -rf build dist
    rm -f eliaApp-PyQt6-2023_12_01.spec

2- Regenere o Executável:

Ative o ambiente virtual, se ainda não estiver ativo.
Instale quaisquer dependências adicionais que você possa ter adicionado ao seu script com pip install.
Execute o PyInstaller novamente para gerar um novo executável com o script atualizado:
    pyinstaller --onefile --windowed eliaApp-PyQt6-2023_12_01.py

Isto irá criar novos diretórios dist/ e build/ e um novo arquivo .spec.

3- Teste o Novo Executável:

Vá para a pasta dist/ e execute o novo arquivo .exe para garantir que as suas alterações foram aplicadas e que tudo está funcionando corretamente.

Lembre-se de que, se você tiver feito alterações substanciais que afetam como os módulos são carregados ou utilizados (por exemplo, adicionar novas importações), você pode precisar ajustar as opções passadas para o PyInstaller, como --hidden-import para novos módulos que não estão sendo automaticamente detectados.

--------------------------------------------------------------------

PARA INCLUIR A PASTA DE IMAGENS "img"
pyinstaller --onefile --windowed --add-data "img/*;img/" eliaApp-05122301.py