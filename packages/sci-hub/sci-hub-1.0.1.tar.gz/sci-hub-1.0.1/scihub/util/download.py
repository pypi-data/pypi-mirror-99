import os
import requests

from webrequests import WebRequest as WR
from simple_loggers import SimpleLogger

from .host import check_host


class SciHub(object):
    def __init__(self, url=None):
        self.logger = SimpleLogger('SciHub')
        self.url = self.check_url(url)

    def check_url(self, url, timeout=5):
        def _check(url):
            try:
                resp = requests.head(url, timeout=timeout)
                elapsed = resp.elapsed.total_seconds()
                self.logger.info(f'good url: {url} [elapsed {elapsed:.3f}s]')
                return elapsed
            except Exception as e:
                self.logger.warning(f'bad url: {url}')

        def _post_url(url):
            soup = WR.get_soup(url)
            post_url = soup.select_one('form[method="POST"]').attrs['action']
            if post_url == '/':
                post_url = url
            self.logger.info(f'post url: {post_url}')
            return post_url

        if url:
            self.logger.info(f'checking url: {url} ...')
            if _check(url):
                return _post_url(url)

        self.logger.info('checking fastest url automaticlly ...')
        hosts, update_time = check_host()
        fastest = 99999999
        for host in hosts:
            elapsed = _check(host)
            if elapsed and elapsed < fastest:
                fastest = elapsed
                url = host
        self.logger.info(f'fastest url: {url} [{fastest}s]')
        return _post_url(url)


    def search(self, term):
        """
            term: URL, PMID, DOI or search string

            return: url of pdf
        """
        self.logger.info(f'searching: {term}')
        payload = {
            'sci-hub-plugin-check': '', 
            'request': term
        }

        soup = WR.get_soup(self.url, method='POST', data=payload)

        pdf = soup.select_one('#pdf')
        captcha = soup.select_one('#captcha')

        if pdf:
            pdf_url = pdf.attrs['src']
        elif captcha:
            captcha_url = captcha.attrs['src']
            print(captcha_url)
        else:
            self.logger.error('your searching string is invalid, please check!')
            return None

        self.logger.info(f'pdf url of "{term}": {pdf_url}')
        return pdf_url


    def download(self, url, outdir='.', filename=None, chunk_size=512):
        filename = filename or os.path.basename(url).split('#')[0]
        if outdir != '.' and not os.path.exists(outdir):
            os.makedirs(outdir)

        outfile = os.path.join(outdir, filename)

        resp = WR.get_response(url, stream=True)
        length = int(resp.headers.get('Content-Length'))
        self.logger.info(f'downloading pdf: {outfile} [{length/1024/1024:.2f} M]')

        with open(outfile, 'wb') as out:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                out.write(chunk)

        self.logger.info(f'save file: {outfile}')



if __name__ == '__main__':
    # sh = SciHub(url='https://scihub.bad')
    # sh = SciHub()
    # sh = SciHub(url='https://sci-hub.ai')
    sh = SciHub(url='https://sci-hub.ee')

    for term in range(26566462, 26566482):
        pdf_url = sh.search(term)
        if pdf_url:
            sh.download(pdf_url)
