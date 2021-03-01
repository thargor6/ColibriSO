package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.Tag;
import com.overwhale.colibri_so.backend.repository.TagRepository;
import com.overwhale.colibri_so.frontend.dto.TagDto;
import com.overwhale.colibri_so.frontend.mapper.TagMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
public class TagService extends CrudService<TagDto, UUID> {
  private final TagRepository repository;

  public TagService(@Autowired TagRepository repository) {
    this.repository = repository;
  }

  public TagDto update(TagDto dto) {
    Tag entity = TagMapper.INSTANCE.dtoToEntiy(dto);
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    } else {
      entity.setLastChangedTime(OffsetDateTime.now());
    }
    return TagMapper.INSTANCE.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<TagDto, UUID> getRepository() {
    return null;
  }

  public Optional<TagDto> get(UUID id) {
    return repository.findById(id).map(e -> TagMapper.INSTANCE.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<TagDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> TagMapper.INSTANCE.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
