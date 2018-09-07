package cn.wangz.webmagic.processor;

import cn.wangz.webmagic.util.ExceptionUtil;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.lang3.StringUtils;
import org.apache.log4j.Logger;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.Site;
import us.codecraft.webmagic.processor.PageProcessor;

import java.util.ArrayList;
import java.util.List;

/**
 * root url:
 * https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28266&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E6%98%8E%E6%98%9F&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn=120&rn=12
 * https://baike.baidu.com/item/%E5%A8%84%E8%89%BA%E6%BD%87
 */
public class BaikeBaiduPageProcessor implements PageProcessor {
    private static final Logger logger = Logger.getLogger(BaikeBaiduPageProcessor.class);

    // 部分一：抓取网站的相关配置，包括编码、抓取间隔、重试次数等
    private Site site = Site.me().setRetryTimes(1).setTimeOut(10000).setSleepTime(5000).setUserAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36");

    @Override
    public void process(Page page) {
        String url = page.getRequest().getUrl();
        try {
            if (url.startsWith("https://sp0.baidu.com/")) {
                List<String> links = getItemList(page.getRawText());
                page.addTargetRequests(links, 10);
            } else if (url.startsWith("https://baike.baidu.com/item/")){
                String value = getContent(page.getHtml().toString());
                page.putField("value", value);
            }
        } catch (Exception e) {
            String msg = ExceptionUtil.stackTraceMsg(e);
            logger.error("process error, msg:" + msg);
        }
    }

    private List<String> getItemList(String content) {
        List<String> urlList = new ArrayList<>();
        JSONObject jsonObject = JSONObject.parseObject(content);
        if (jsonObject == null || !jsonObject.containsKey("data")) return urlList;
        JSONArray jsonArray = jsonObject.getJSONArray("data");
        if (jsonArray == null || jsonArray.isEmpty()) return urlList;
        for (int i = 0; i < jsonArray.size(); i++) {
            JSONObject dataObject = jsonArray.getJSONObject(i);
            if (!dataObject.containsKey("result")) continue;
            JSONArray resultArray = dataObject.getJSONArray("result");
            for (int j = 0; j < resultArray.size(); j++) {
                String ename = resultArray.getJSONObject(j).getString("ename");
                if (ename != null && StringUtils.isNotBlank(ename)) {
                    String url = "https://baike.baidu.com/item/" + ename;
                    urlList.add(url);
                }
            }
        }
        return urlList;
    }

    private String getContent(String html) {
        Document document = Jsoup.parse(html);
        String content = document.select("div.para").text();
        return content;
    }

    @Override
    public Site getSite() {
        return site;
    }


}
