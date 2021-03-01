package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.SnippetTag;
import com.overwhale.colibri_so.backend.repository.SnippetTagRepository;
import com.overwhale.colibri_so.frontend.dto.SnippetTagDto;
import com.overwhale.colibri_so.frontend.mapper.SnippetTagMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.Optional;
import java.util.UUID;

@Service
public class SnippetTagService extends CrudService<SnippetTagDto, UUID> {
  private final SnippetTagRepository repository;

  public SnippetTagService(@Autowired SnippetTagRepository repository) {
    this.repository = repository;
  }

  public SnippetTagDto update(SnippetTagDto dto) {
    SnippetTag entity = SnippetTagMapper.INSTANCE.dtoToEntiy(dto);
    return SnippetTagMapper.INSTANCE.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<SnippetTagDto, UUID> getRepository() {
    return null;
  }

  public Optional<SnippetTagDto> get(UUID id) {
    return repository.findById(id).map(e -> SnippetTagMapper.INSTANCE.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<SnippetTagDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> SnippetTagMapper.INSTANCE.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
