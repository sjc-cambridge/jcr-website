from website import create_site

app = create_site()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
