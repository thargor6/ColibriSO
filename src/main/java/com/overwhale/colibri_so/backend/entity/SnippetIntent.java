package com.overwhale.colibri_so.backend.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import java.util.UUID;

@Entity
@Data
@Table(name = "snippet_intents")
@IdClass(SnippetIntentKey.class)
public class SnippetIntent {
  @NotNull
  @Id
  @Type(type = "uuid-char")
  private UUID snippetId;

  @NotNull
  @Id
  @Type(type = "uuid-char")
  private UUID intentId;
}
