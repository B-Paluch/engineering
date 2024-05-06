package prz.paluch.fileuploader.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import prz.paluch.fileuploader.entity.FileEntity;

@Repository
public interface FileRepository extends JpaRepository<FileEntity, String> {
}
