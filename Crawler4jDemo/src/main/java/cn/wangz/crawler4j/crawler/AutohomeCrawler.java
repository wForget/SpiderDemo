package cn.wangz.crawler4j.crawler;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.url.WebURL;

/**
 * Created by wangz on 2018/8/7.
 * 汽车之家
 * https://www.autohome.com.cn
 */
public class AutohomeCrawler extends WebCrawler {

    @Override
    public boolean shouldVisit(Page referringPage, WebURL url) {
        return false;
    }

    @Override
    public void visit(Page page) {

    }
}
