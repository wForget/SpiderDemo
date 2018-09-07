package cn.wangz.webmagic.job;

import cn.wangz.webmagic.pipeline.SimpleFilePipeline;
import cn.wangz.webmagic.processor.BaikeBaiduPageProcessor;
import us.codecraft.webmagic.Spider;
import us.codecraft.webmagic.scheduler.PriorityScheduler;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by hadoop on 2018/9/7.
 */
public class BaikeBaiduJob {
    public static void main(String[] args) {
        List<String> urlList = new ArrayList<>();

        for (int i = 0; i <= 500; i++) {
            String url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28266" +
                    "&from_mid=1" +
                    "&format=json" +
                    "&ie=utf-8" +
                    "&oe=utf-8" +
                    "&query=%E6%98%8E%E6%98%9F" +
                    "&sort_key=" +
                    "&sort_type=1" +
                    "&stat0=" +
                    "&stat1=" +
                    "&stat2=" +
                    "&stat3=" +
                    "&pn=" + i * 12 +
                    "&rn=12";
            urlList.add(url);
        }
        Spider.create(new BaikeBaiduPageProcessor())
                .setScheduler(new PriorityScheduler())  //Scheduler是用来维护Url队列，PriorityScheduler可以控制url优先级
                .addUrl(urlList.toArray(new String[urlList.size()]))
                .addPipeline(new SimpleFilePipeline("E:\\test\\baike"))
                .thread(1)
                .run();
    }
}
