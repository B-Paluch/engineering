package prz.paluch.logs.controllers;

import lombok.RequiredArgsConstructor;
import org.springframework.cloud.stream.function.StreamBridge;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import prz.paluch.logs.entity.LogDTO;
import prz.paluch.logs.entity.LogEntity;
import prz.paluch.logs.repositories.LogRepository;

import java.util.List;
import java.util.function.Consumer;

@RequiredArgsConstructor
@RestController
public class LogController {
    private final LogRepository repository;
    private final StreamBridge streamBridge;

    @PostMapping
    public String save(@RequestBody LogEntity entity) {
        repository.save(entity);
        streamBridge.send(
                "log-out-0",
                LogEntity.builder().service("log-service").logValue("someone used rest endpoint. with message: " +
                        entity.toString()
                        +" What a quack.").build()
        );
        return "log saved:" + entity.toString();
    }

    @GetMapping
    public List<LogEntity> get() {
        return repository.findAll();
    }

    @Bean
    public Consumer<LogDTO> logIt() {
        return data-> {
            System.out.println("logging!");
            System.out.println(data);
            var k = repository.save(LogEntity.builder().logValue(data.getValue()).service(data.getService()).build());
            System.out.println(k);
        };
    }
}
