package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.Tag;
import com.overwhale.colibri_so.backend.repository.TagRepository;
import com.overwhale.colibri_so.frontend.dto.TagDto;
import com.overwhale.colibri_so.frontend.mapper.TagMapper;
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
  private final TagMapper tagMapper;

  public TagService(TagRepository repository, TagMapper tagMapper) {
    this.repository = repository;
    this.tagMapper = tagMapper;
  }

  public TagDto update(TagDto dto) {
    Tag entity = tagMapper.dtoToEntiy(dto);
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    }
    entity.setLastChangedTime(OffsetDateTime.now());
    return tagMapper.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<TagDto, UUID> getRepository() {
    return null;
  }

  public Optional<TagDto> get(UUID id) {
    return repository.findById(id).map(e -> tagMapper.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<TagDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> tagMapper.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
