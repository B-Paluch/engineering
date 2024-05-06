package prz.paluch.fileuploader.entity;

import lombok.*;
import org.apache.kafka.common.protocol.types.Field;

@AllArgsConstructor
@RequiredArgsConstructor
@Getter
@Setter
@Builder
public class ResponseFileEntity {
    private String name;
    private String url;
    private String type;
    private long size;
}
