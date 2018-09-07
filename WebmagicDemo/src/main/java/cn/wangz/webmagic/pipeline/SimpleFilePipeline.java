package cn.wangz.webmagic.pipeline;

import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import us.codecraft.webmagic.ResultItems;
import us.codecraft.webmagic.Task;
import us.codecraft.webmagic.pipeline.Pipeline;
import us.codecraft.webmagic.utils.FilePersistentBase;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

/**
 * Created by hadoop on 2018/9/7.
 */
public class SimpleFilePipeline extends FilePersistentBase implements Pipeline {

    private Logger logger = LoggerFactory.getLogger(getClass());

    /**
     * create a SimpleFilePipeline with default path"/data/webmagic/"
     */
    public SimpleFilePipeline() {
        setPath("/data/webmagic/");
    }

    public SimpleFilePipeline(String path) {
        setPath(path);
    }

    @Override
    public void process(ResultItems resultItems, Task task) {
        String path = this.path + PATH_SEPERATOR + task.getUUID() + PATH_SEPERATOR;
        if (!resultItems.getAll().containsKey("value") || StringUtils.isBlank(resultItems.get("value").toString())) return;
        try {
            PrintWriter printWriter = new PrintWriter(new OutputStreamWriter(new FileOutputStream(getFile(path + DigestUtils.md5Hex(resultItems.getRequest().getUrl()) + ".html")),"UTF-8"));
            printWriter.println(resultItems.get("value").toString());
//            printWriter.println("url:\t" + resultItems.getRequest().getUrl());
//            for (Map.Entry<String, Object> entry : resultItems.getAll().entrySet()) {
//                if (entry.getValue() instanceof Iterable) {
//                    Iterable value = (Iterable) entry.getValue();
//                    printWriter.println(entry.getKey() + ":");
//                    for (Object o : value) {
//                        printWriter.println(o);
//                    }
//                } else {
//                    printWriter.println(entry.getKey() + ":\t" + entry.getValue());
//                }
//            }
            printWriter.close();
        } catch (IOException e) {
            logger.warn("write file error", e);
        }
    }
}
